# -*- coding: utf-8 -*-
"""
Created on Wed Apr 17 11:09:38 2019

@author: ASUS R0GS
"""

import nltk
print("Sentence: ", end="")
a = nltk.word_tokenize(input())
print(nltk.tag.pos_tag(a,tagset="universal"))