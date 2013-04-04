#!/usr/bin/python
# -*- coding: utf8 -*-

# Z.E.R = Zero Eyes Required
# Games playable just with your voice
# Author: Alfonso E.M. <alfonso@el-magnifico.org>
# License: Free (GPL2) 
# Version: 1.0 - 4/Apr/2013

import sys
from configobj import ConfigObj

sys.path.append("./lib")

import Voice

# Main
def main():

# Load main config file
    CONF = ConfigObj("zer.conf")

    SYNTH = Voice.Synth(CONF['SYNTH'])
    RECOG = Voice.Recog()

    while True:
      SYNTH.say("How many players?")
      confidence,answer=RECOG.listen()
      nplayers=int(answer)
      print "Players:", nplayers
      players=[]
      for n in range(1,nplayers+1):
          print n
          SYNTH.say("What is the name of player "+str(n)+"?" )
          confidence,answer=RECOG.listen()
          SYNTH.say("Player "+str(n)+" is "+answer)
          players.append(answer)
      
      SYNTH.close()
      break

if __name__ == '__main__':
  main()
 
