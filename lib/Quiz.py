#!/usr/bin/python
# -*- coding: utf8 -*-

# Z.E.R = Zero Eyes Required
# Games playable just with your voice
# Author: Alfonso E.M. <alfonso@el-magnifico.org>
# License: Free (GPL2) 
# Version: 1.0 - 4/Apr/2013

import random

class SimpleQuiz:
    def __init__(self,filename):

        self._questions=[]
        self._answers=[]

        f = open(filename)
        for line in f:
            if len(line)>4 and line.find(":")>1:
                question,answer=line.split(":")
                self._questions.append(unicode(question,"utf_8"))
                self._answers.append(unicode(answer,"utf_8"))
        self.selected_question=-1
        return

    def get_question(self):
        self.selected_question=random.randint(0, len(self._questions)-1)
#        print "Selected question %i de %i" % (self.selected_question+1,len(self._questions))
        return self._questions[self.selected_question]

    def get_answer(self):
        return self._answers[self.selected_question]
 
    def _normalize(self,txt):
        txt=txt.strip().lower()
        txt=txt.encode("ascii",errors='replace')
        return txt

    def check_answer(self,answer):
        if self._normalize(answer) == self._normalize(self.get_answer()):
            return True
        else:
            return False

