# -*- coding: utf-8 -*-
"""
Created on Sun Mar 12 07:13:56 2017

This is for testing BaseFantasyClasses.

@author: lenhart
"""

from BaseClasses.BaseFantasyClasses import HitterFile


def test1():
    guys1 = open("FGDepthProjections2017.csv", 'r')
    guys2 = open("newProjections.csv",'w')
    header = 0
    guys2.write(guys1.readline()[3:])
    for line in guys1:
        guys2.write(line)
    guys1.close()
    guys2.close()
    guys2 = open("newProjections.csv",'r')
    guys1 = open("FGDepthProjections2017.csv", 'w')
    guys1.write(guys2.read())
    
def test():
    guys = HitterFile("FGDepthProjections2017.csv")
    print(guys.file.fieldnames)
    print(guys[1].printPlayer())
    print(guys.replacementLevel())
    for i in range(100):
        print("{:18} fWAR(): {:5}".format(guys[i].name,guys[i].fWAR()))
    
    
test()