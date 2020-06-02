# -*- coding: utf-8 -*-
"""
Created on Wed Mar 15 22:56:18 2017

This very simple script looks to see if it needs to rename some files for your 
draft assistant.

@author: lenhart
"""

import os

def manageFiles():
    #print(os.getcwd())
    #print(os.listdir('Files'))
    if 'stats.csv' in os.listdir('Files'):
        #print("I found the secret documents!")
        if 'stats (1).csv' in os.listdir('Files'):
            a = str(len(os.listdir('Files')))
            os.rename('Files/stats.csv', 'Files/stats'+a+'.csv')
            os.rename('Files/stats (1).csv','Files/stats.csv')
    if 'TrueTalent.csv' in os.listdir('Files'):
        #print("I found the secret documents!")
        if 'TrueTalent (1).csv' in os.listdir('Files'):
            a = str(len(os.listdir('Files')))
            os.rename('Files/TrueTalent.csv', 'Files/TrueTalent'+a+'.csv')
            os.rename('Files/TrueTalent (1).csv','Files/TrueTalent.csv')
        
    
    
    
#manageFiles()
