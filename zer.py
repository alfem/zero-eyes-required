#!/usr/bin/python
# -*- coding: utf8 -*-

# Z.E.R = Zero Eyes Required
# Games playable just with your voice
# Author: Alfonso E.M. <alfonso@el-magnifico.org>
# License: Free (GPL2) 
# Version: 1.0 - 4/Apr/2013

import sys
from configobj import ConfigObj
import random

# Load main config file
CONF = ConfigObj("zer.conf")

sys.path.append("./lib")
import Voice
import Quiz


def dialog(key):
    if key in CONF["DIALOGS"]:
        return random.choice(CONF["DIALOGS"][key])
    else:
        return "No dialog defined in configuration file"

# MAIN
def main():

    SYNTH = Voice.Synth(CONF['SYNTH'])
    RECOG = Voice.Recog(CONF['RECOG'])
    QUIZ = Quiz.SimpleQuiz(CONF['quiz'])

    while True:
      SYNTH.say(dialog("ask_for_players"))
      confidence,answer=RECOG.listen()
      players=answer.split()
      nplayers=len(players)
      print "Players: ", nplayers
      SYNTH.say(dialog("players") % nplayers)

      SYNTH.say(dialog("start_the_game"))

      for n in range(0,nplayers):
          SYNTH.say(dialog("ask_player") % players[n])
          SYNTH.say(QUIZ.get_question())
          confidence,answer=RECOG.listen()

          if answer==CONF["quit_command"]:
              break

          if QUIZ.check_answer(answer):
              SYNTH.say(dialog("answer_is_right"))
          else: 
              SYNTH.say(dialog("answer_is_wrong"))
              SYNTH.say(dialog("the_right_answer_is") % QUIZ.get_answer())  
           
      SYNTH.close()
      break

if __name__ == '__main__':
  main()
 
