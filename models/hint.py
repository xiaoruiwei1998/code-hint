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
import json
from collections import deque
import sys
from tqdm import tqdm
from multiprocessing import connection
# from langchain.llms import OpenAI
# llm = OpenAI(openai_api_key="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")

with open("./config/prompt_config.json", "r") as f:
    prompt_config = json.load(f)
    
with open("./config/llm_config.json", "r") as f:
    llm_config = json.load(f)

class Hint(object):
    
    def __init__(self, problem_desc="", code="", input_data="", output_data="", requirement="multiple_hint_prompt", levels=["orientation", "instrumental", "worked_example", "bottom_out"], constraints=["length", "knowledge"], format="fence", example_user_prompt="", example_feedback=""):
        
        self.model = llm_config['gpt_config']['model']
        self.code = code
        self.api_key = llm_config['gpt_config']['api_key']
        self.levels = levels
        self.levels_desc = ""
        for i in range(len(self.levels)):
            self.levels_desc += "\n" + str(i+1) + ". "
            self.levels_desc += prompt_config['levels'][levels[i]]
            self.levels_desc += "\n"
        self.constraints = ""
        for constraint in constraints:
            self.constraints += prompt_config['constraints'][constraint]
        self.prompt = prompt_config['requirement'][requirement] \
        + self.levels_desc \
        + "\n Problem Description: \n" + problem_desc \
        + "\n Input: \n" + input_data \
        + "\n Expected Output: \n" + output_data \
        + "\n Constraints: \n" + self.constraints \
        + prompt_config['format'][format]
        self.example_user_prompt = example_user_prompt
        self.example_feedback = example_feedback
        self.hint = {level: "" for level in levels}
        self.current_user_message = ""
        
    def generateGPTAnswer(self):
        openai.api_key = self.api_key
        messages = [
            {
                # instruction, problem information
                "role": "system",
                "content": self.prompt
            },
            
            {
                # example code
                "role": "user",
                "content": self.example_user_prompt
            },
            
            {
                # example feedback
                "role": "assistant",
                "content": self.example_feedback
            },
            
            {
                # code
                "role": "user",
                "content": self.code
            }
        ]
        response = openai.ChatCompletion.create(
        model=self.model,
        messages=messages,
        seed=0,
        temperature=0,
        )
        raw_hints = response["choices"][0]['message']['content']
        print(raw_hints)
        raw_hints = raw_hints.split("---------------------")[1:]
        raw_hints = [hint for hint in raw_hints if "hint here" not in hint] 
        
        self.hint = {
            "orientation": raw_hints[0].strip(),
            "instrumental": raw_hints[1].strip(),
            "worked_example": raw_hints[2].strip(),
            "bottom_out": raw_hints[3].strip()
        }
        return json.dumps(self.hint)