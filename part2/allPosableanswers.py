# -*- coding: utf-8 -*-
"""Untitled1.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1UyiofK2aE-P1OqI3YYjv3wosRRwJRGHm
"""

import copy

def next_woman(woman,items,str):
  print (woman)
  for nam in woman:
    print (nam)
    temp=copy.deepcopy(woman)
    next_item(temp.remove(nam),items,str+nam+" ")

def next_item(woman,items,str):
  print (woman)
  if len(items)==1:
   # with open("pass.txt", "a") as myfile:
    #  myfile.write(str+items[0])
    print (str+items[0])
  for ite in items:
    temp=copy.deepcopy(items)
    next_woman(woman,temp.remove(ite),str+ite+" ")


wom=["Germain","Lovelace","Franklin","Curie","Noether"]
item=["telescope","abacus","laptop","pencil","scales"]
str=""
next_woman(wom,item,str)