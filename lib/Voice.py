#!/usr/bin/python
# -*- coding: utf8 -*-

# Z.E.R = Zero Eyes Required
# Games playable just with your voice
# Author: Alfonso E.M. <alfonso@el-magnifico.org>
# License: Free (GPL2) 
# Version: 1.0 - 4/Apr/2013

import audiotools

from sys import byteorder
from array import array
from struct import pack

import pyaudio
import wave

import urllib2, os
import simplejson

# For voice synthesys
#import speechd
import subprocess  #temporary solution to speechd bug

class Synth:
    def __init__(self,CONF):
        print "Using "+CONF["module"],CONF["voice"],"voice"
        self.module=CONF["module"]
        self.voice=CONF["voice"]
#        self.client=speechd.SSIPClient('zer')
#        self.client.set_output_module(CONF["module"])
#        self.client.set_language(CONF["language"])
#        self.client.set_pitch(int(CONF["pitch"]))
#        self.client.set_rate(int(CONF["rate"]))
#        self.client.set_synthesis_voice(CONF["voice"])
#        self.client.set_punctuation(speechd.PunctuationMode.SOME)
        return

    def say(self,text):
      print "I say:", text
#      self.client.speak(text)
      if self.module=="espeak":
          subprocess.call('espeak -v'+self.voice+' "'+text+'" 2>/dev/null', shell=True)
      elif self.module=="festival":
          subprocess.call('echo "'+text+'"|festival --tts', shell=True)



    def close(self):
      self.client.close()

class Recog:
    def __init__(self,CONF):

        self.language = CONF['language']
        self.threshold = CONF['silence_level']
        self.chunk_size = 1024
        self.format = pyaudio.paInt16
        self.rate = 16000

        return

    def listen(self):
        print "Listening..."
        text=unicode(raw_input(),"utf-8")
        return 100,text
        self.record_to_file("/tmp/zer.wav")
        print "Voice recorded to wav. Converting to flac..."
        self._wav_to_flac("/tmp/zer.wav","/tmp/zer.flac")
        json_answer=self._recognize_flac("/tmp/zer.flac")
        js=simplejson.loads(json_answer)
        confidence=js['hypotheses'][0]['confidence']
        text=js['hypotheses'][0]['utterance']
        print "You say:", text
        return confidence,text

    def _recognize_flac(self,filename):
        print "Recognizing..."
        url = 'https://www.google.com/speech-api/v1/recognize?lang='+self.language+'&client=chromium'
        length = os.path.getsize(filename)
        filedata = open(filename, "rb")
        request = urllib2.Request(url, data=filedata)
        request.add_header('Cache-Control', 'no-cache')
        request.add_header('Content-Length', '%d' % length)
        request.add_header('Content-Type', 'audio/x-flac; rate=16000')
        res = urllib2.urlopen(request).read().strip()
        return res


    def _print_progress(self,x,y):
        print "%d%%" % (x*100/y)

    def _wav_to_flac(self,w,f):
        audiotools.open(w).convert(f,audiotools.FlacAudio,progress=self.print_progress)
        return


    def _is_silent(self,snd_data):
        return max(snd_data) < self.threshold

    def _normalize(self,snd_data):
        maximun = 16384
        times = float(maximun)/max(abs(i) for i in snd_data)

        r = array('h')
        for i in snd_data:
            r.append(int(i*times))
        return r

    def trim(self,snd_data):
        def _trim(snd_data):
            snd_started = False
            r = array('h')

            for i in snd_data:
                if not snd_started and abs(i)>self.threshold:
                    snd_started = True
                    r.append(i)

                elif snd_started:
                    r.append(i)
            return r

        # Trim left
        snd_data = _trim(snd_data)

        # Trim right
        snd_data.reverse()
        snd_data = _trim(snd_data)
        snd_data.reverse()
        return snd_data

    def _add_silence(self,snd_data, seconds):
        r = array('h', [0 for i in xrange(int(seconds*self.rate))])
        r.extend(snd_data)
        r.extend([0 for i in xrange(int(seconds*self.rate))])
        return r

    def record(self):
        p = pyaudio.PyAudio()
        stream = p.open(format=self.format, channels=1, rate=self.rate,
            input=True, output=True,
            frames_per_buffer=self.chunk_size)

        num_silent = 0
        snd_started = False

        r = array('h')

        while 1:
            snd_data = array('h', stream.read(self.chunk_size))
            if byteorder == 'big':
                snd_data.byteswap()
            r.extend(snd_data)

            silent = self._is_silent(snd_data)

            if silent and snd_started:
                num_silent += 1
            elif not silent and not snd_started:
                snd_started = True

            if snd_started and num_silent > 30:
                break

        sample_width = p.get_sample_size(self.format)
        stream.stop_stream()
        stream.close()
        p.terminate()

        r = self._normalize(r)
        r = self.trim(r)
        r = self._add_silence(r, 0.5)
        return sample_width, r

    def record_to_file(self,filename):
        sample_width, data = self.record()
        data = pack('<' + ('h'*len(data)), *data)

        wf = wave.open(filename, 'wb')
        wf.setnchannels(1)
        wf.setsampwidth(sample_width)
        wf.setframerate(self.rate)
        wf.writeframes(data)
        wf.close()




