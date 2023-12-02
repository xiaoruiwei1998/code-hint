import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import openai
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
    
    def __init__(self, problem_desc="", code="", input_data="", output_data="", requirement="multiple_hint_prompt", levels=["orientation", "instrumental", "worked_example", "bottom_out"], constraints=["length", "knowledge"], format="fence", example_user_prompt="", example_feedback="", subgoals="", hint_type="summative"):
        
        self.model = llm_config['gpt_config']['model']
        self.code = code
        self.api_key = llm_config['gpt_config']['api_key']
        self.levels = levels
        self.levels_desc = ""
        self.subgoals = "import csv; open csv file with correct path; read csv file into a 2-D list; looping over each line; looping over each column; determine the appropriate data structure (dict) to keep counting; find the value we want from the dict"
        for i in range(len(self.levels)):
            if i == 1:
                self.levels_desc += self.subgoals
            self.levels_desc += "\n" + str(i+1) + ". "
            self.levels_desc += prompt_config['levels'][levels[i]]
            self.levels_desc += "\n"
        self.constraints = ""
        for constraint in constraints:
            self.constraints += prompt_config['constraints'][constraint]
        
        self.example_user_prompt = example_user_prompt
        self.example_feedback = example_feedback
        self.hint = {level: "" for level in levels}
        self.current_user_message = ""
        self.hint_type = hint_type
        
        if self.hint_type == "summative": 
            self.prompt = "Generate the code and explanation to this problem. The code should be as similar to the student's solution as possible:" \
            + "\n Problem Description: \n" + problem_desc \
            + "\n Input: \n" + input_data \
            + "\n Expected Output: \n" + output_data \
            + "The entire response should not exceed 50 lines, and the code should not exceed 20 lines (comments do not count). use import csv f = open(file_path, 'r') data = list(csv.reader(f)) to read data from csv file."
        
        if self.hint_type == "multilevel":
            self.prompt = prompt_config['requirement'][requirement] \
            + self.levels_desc \
            + "\n Problem Description: \n" + problem_desc \
            + "\n Input: \n" + input_data \
            + "\n Expected Output: \n" + output_data \
            + "\n Constraints: \n" + self.constraints \
            + prompt_config['format'][format]
        
    def generateGPTAnswer(self):
        openai.api_key = self.api_key
        if self.hint_type == "summative":
            messages = [
                {
                    # instruction, problem information
                    "role": "system",
                    "content": self.prompt
                },
                {
                    # code
                    "role": "user",
                    "content": self.code
                }
            ]
        if self.hint_type == "multilevel":
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
        
        if self.hint_type == "multilevel":
            raw_hints = raw_hints.split("---------------------")[1:]
            raw_hints = [hint for hint in raw_hints if "hint here" not in hint] 
            
            self.hint = {
                "orientation": raw_hints[0].strip(),
                "instrumental": raw_hints[1].strip(),
                "worked_example": raw_hints[2].strip(),
                "bottom_out": raw_hints[3].strip()
            }
        
        if self.hint_type == "summative":
            self.hint = {"summative":raw_hints} # for control condition
        return json.dumps(self.hint)