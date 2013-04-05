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
      if answer==CONF["quit_command"]:
          break

      players=answer.split()
      nplayers=len(players)
      score=[0 for x in range(nplayers)]

      print "Players: ", nplayers
      SYNTH.say(dialog("players") % nplayers)

      SYNTH.say(dialog("start_the_game"))

      while True:
          for n in range(0,nplayers):
              SYNTH.say(dialog("ask_player") % players[n])
              question=QUIZ.get_question()
              SYNTH.say(question)
              confidence,answer=RECOG.listen()

              if answer==CONF["quit_command"]:
                  break

              elif answer==CONF["repeat_command"]:
                  SYNTH.say(dialog("repeat"))
                  SYNTH.say(question)
                  confidence,answer=RECOG.listen()

              elif answer==CONF["score_command"]:
                  for p in range(0,nplayers):
                      print dialog("score_of_player"), players[p],score[p]
                      SYNTH.say(dialog("score_of_player") % (players[p],score[p]))
                      confidence,answer=RECOG.listen()

              if QUIZ.check_answer(answer):
                  SYNTH.say(dialog("answer_is_right"))
                  score[n]+=1
              else: 
                  SYNTH.say(dialog("answer_is_wrong"))
                  SYNTH.say(dialog("the_right_answer_is") % QUIZ.get_answer())  

          if answer==CONF["quit_command"]:
              break

          SYNTH.say(dialog("mumbojumbo"))  
           
#      SYNTH.close()
      break

if __name__ == '__main__':
  main()
 
