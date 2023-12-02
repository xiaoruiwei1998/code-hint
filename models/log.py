import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from collections import deque
import sys
from tqdm import tqdm
from multiprocessing import connection
import json

class Log(object):
    
    def __init__(self, student_id, problem_id, code, event_type, event_time, event_log):
        self.student_id = 0
        self.problem_id = problem_id
        self.code = code
        self.event_type = event_type
        self.event_time = event_time
        self.event_log = str(event_log)
    
 
    
    def write_to_db(self, conn):
        create_table(conn)
        sql = """
        INSERT INTO LOGS (STU_ID, PROBLEM_ID, CODE, EVENT_TYPE, EVENT_TIME, EVENT_LOG) 
        VALUES (?, ?, ?, ?, ?, ?)
        """
        # Tuple of values to insert
        values = (self.student_id, self.problem_id, self.code, self.event_type, self.event_time, self.event_log)

        print(values)
        # # Execute the SQL statement
        conn.execute(sql, values)
        conn.commit() 
        
        
def create_table(conn):
    sql = """
        CREATE TABLE IF NOT EXISTS LOGS (
            STU_ID INTEGER,
            PROBLEM_ID INTEGER,
            CODE TEXT,
            EVENT_TYPE TEXT,
            EVENT_TIME TEXT,
            EVENT_LOG TEXT
        )
        """
    conn.execute(sql)
    conn.commit()