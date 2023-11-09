import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import openai
import re
import difflib
import os
import time
import argparse
import ast
import itertools
from collections import deque
import sys
from tqdm import tqdm
from multiprocessing import connection
import json

class Problem(object):
    
    def __init__(self):
        self.idx = 1
        self.problem_desc = "You are a tiktok dancing influencer, and you want to know the best hashtags to post videos to attract maximum views. You have the data for top10 trending dancing videos in top10videos.csv. You want to know what is the most used hashtag(s) by trending videos, and your task is creating a dictionary to store the number of occurrences for each hashtag."
        self.code = """file_path = 'coding_problems/tiktok/top10videos.csv'
hashtag_count = {}
print(hashtag_count)"""
        self.input = """
        author,videoID,videoTitle,Views,publishTime,duration,Hashtags,Likes,Shares,Comments,Music,Description
JaneDoe,tv001,Electro Swing,150000,2023-01-15,3:50,"#electro,#swing,#dance,#trending,#viral,#party,#fun,#summer",70000,5500,5000,ElectroTunes,Join the electro swing party!
JohnDance,tv002,Hip Hop Challenge,175000,2023-02-10,4:20,"#hiphop,#challenge,#dance,#viral,#duet,#moves,#street",80000,6000,5900,HipHopBeats,Show me your best hip-hop moves!
LucyLu,tv003,Ballet Dreams,200000,2023-03-05,5:15,"#ballet,#dreams,#dance,#trending,#classic,#elegance",82000,6400,6200,ClassicWaltz,My ballet journey!
MikeMoves,tv004,Street Dance Revolution,190000,2023-03-20,4:45,"#streetdance,#revolution,#moves,#freestyle,#viral,#duet",79000,6300,6100,StreetBeat,Taking street dance to the next level!
AnnaGroove,tv005,Latin Vibes,165000,2023-04-10,3:30,"#latin,#vibes,#dance,#salsa,#trending",71000,5600,5200,LatinBeat,Feel the rhythm with me!
DanceMaster,tv101,Salsa Fiesta,210000,2023-05-15,3:10,"#salsa,#fiesta,#latin,#dance,#hit,#viral,#groove,#night",105000,4500,6800,HotSalsa,Let's salsa all night!
GroovyGal,tv102,Retro Dance,250000,2023-06-12,4:05,"#retro,#oldies,#dance,#viral,#party,#classic,#throwback",120000,4800,7100,RetroHits,Bringing back the golden era!
StepKing,tv103,Tap Dance Tunes,180000,2023-07-10,3:45,"#tapdance,#tunes,#rhythm,#dance,#viral,#tap,#beats",90000,4600,6500,TapBeats,Tap along with me!
HipsterHop,tv104,Urban Beats,230000,2023-08-15,4:20,"#urban,#beats,#hiphop,#dance,#street,#viral,#citylife",110000,4900,7000,UrbanSounds,Street dance like never before!
TwirlTwist,tv105,Bollywood Bash,240000,2023-09-05,4:50,"#bollywood,#bash,#indian,#dance,#festive,#viral,#colorful",115000,5000,7200,BollywoodBeats,Dance to the Bollywood rhythm!
"""
        self.output = "{'#dance': 9, '#viral': 8, '#trending': 3, '#party': 2, '#hiphop': 2, '#duet': 2, '#moves': 2, '#street': 2, '#classic': 2, '#latin': 2, '#salsa': 2, '#beats': 2, '#electro': 1, '#swing': 1, '#fun': 1, '#summer': 1, '#challenge': 1, '#ballet': 1, '#dreams': 1, '#elegance': 1, '#streetdance': 1, '#revolution': 1, '#freestyle': 1, '#vibes': 1, '#fiesta': 1, '#hit': 1, '#groove': 1, '#night': 1, '#retro': 1, '#oldies': 1, '#throwback': 1, '#tapdance': 1, '#tunes': 1, '#rhythm': 1, '#tap': 1, '#urban': 1, '#citylife': 1, '#bollywood': 1, '#bash': 1, '#indian': 1, '#festive': 1, '#colorful': 1}"
        self.example_user_prompt = """[example-code]
file_path = 'coding_problems/tiktok/top10videos.csv'
hashtag_count = {}
import csv
with open(file_path, 'r') as file:  # open file
    reader = csv.reader(file) # read file 
    data = list(reader) # store data to a list 
    print(data) # print data to debug
    [end-example-code]"""
        self.example_feedback = """[example-feedback]
        ###### This is a very good start, but your code is incompleted. You have successfully read csv file into a 2-D list, and your next step is to loop over the list. 
        ###### You are on the right track! The next step to do is reading each row (1-D lists) from the data (a 2-D list), and you may want to use for-loop.
        ###### Your code is a good start, and you might want to learn the next step from this example:
        for row in data: # data is a 2-d list, each item in data is an 1-d list
            print(row) # see the structure of each row
            col_0 = row[0] # get the value on (row_0, col_0)
        ###### Your code is a good start, and here we implemented the next step for you:
file_path = 'coding_problems/tiktok/top10videos.csv'
hashtag_count = {}
import csv
with open(file_path, 'r') as file:  # open file
    reader = csv.reader(file) # read file 
    data = list(reader) # store data to a list 
    print(data) # print data to debug
    for row in data[1]: # exclude the first line (column names). The data is a 2-d list, each item in data is an 1-d list
        hashtags = row[6] # the 6th column stores hashtags
        ######[end-example-feedback]"""
        
            
    def get_problem(self):
        return json.dumps({"problem_desc":self.problem_desc, "code": self.code, "input": self.input, "output": self.output, "example_user_prompt": self.example_user_prompt, "example_feedback": self.example_feedback})
    
    def update_code(self, updated_code):
        self.code = updated_code