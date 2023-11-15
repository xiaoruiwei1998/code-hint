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
        self.problem_id = 0
        self.problem_title = ""
        self.problem_desc = ""
        self.code = """"""
        self.subgoals = """"""
        self.input = """"""
        self.output = ""
        self.example_user_prompt = """"""
        self.example_feedback = """"""
       
        
    def write_to_db(self, conn):
         
        sql = """
        INSERT INTO PROBLEMS (PROBLEM_ID, PROBLEM_DESC, CODE, INPUTS, OUTPUTS, EXAMPLE_USER_PROMPT, EXAMPLE_FEEDBACK, SUBGOALS) 
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """
        # Tuple of values to insert
        values = (self.problem_id, self.problem_desc, self.code, self.input, self.output, self.example_user_prompt, self.example_feedback, self.subgoals)

        # Execute the SQL statement
        conn.execute(sql, values)
        conn.commit()      
    
    def get_problem(self, problem_id, cursor):
        
        query = "SELECT * FROM problems WHERE PROBLEM_ID = " + str(problem_id)
        cursor.execute(query)
        problem = cursor.fetchall()[0]
        
        self.problem_id = problem[0]
        self.problem_title = problem[1]
        self.problem_desc = problem[2]
        self.code = problem[3]
        self.subgoals = problem[8]
        self.input = problem[4]
        self.output = problem[5]
        self.example_user_prompt = problem[6]
        self.example_feedback = problem[7]
        return json.dumps({"problem_desc":self.problem_desc, "code": self.code, "input": "A csv file.", "output": self.output, "example_user_prompt": self.example_user_prompt, "example_feedback": self.example_feedback, "problem_title":self.problem_title, "problem_subgoals":self.subgoals})
    
    def update_code(self, updated_code):
        self.code = updated_code