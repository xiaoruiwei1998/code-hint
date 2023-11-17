from flask import Flask, render_template, request, jsonify
import requests
import sys
import subprocess
import openai
from models.hint import Hint
from models.problem import Problem
from models.log import Log
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

problem = Problem()
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

import sqlite3

    
    
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/run_code', methods=['POST'])
def run_code():
    code = request.json['code']
    try:
        output = subprocess.check_output(["python3", "-c", code], stderr=subprocess.STDOUT, timeout=5).decode()
    except subprocess.CalledProcessError as e:
        output = e.output.decode()
    except Exception as e:
        output = str(e)
    return jsonify({"output": output})

@app.route('/get_hint', methods=['POST'])
def get_hint():
    problem_desc = request.json.get('problemDesc')
    code = request.json.get('code')
    hint = Hint(problem_desc=problem_desc, code=code, input_data=problem.input, output_data=problem.output, example_user_prompt=problem.example_user_prompt, example_feedback=problem.example_feedback)
    print(hint)
    response = hint.generateGPTAnswer()
    if response:
        return jsonify(hints = response)
    else:
        return jsonify({"error": "Failed to get hint"}), 500
    
@app.route('/get_problem', methods=['POST'])
def get_problem():
    
    conn = sqlite3.connect("./db/problems_db.sqlite", check_same_thread=False)
    problem_idx = request.json.get('idx')
    problem = Problem()
    cursor = conn.cursor()
    problem_info = problem.get_problem(problem_idx, cursor)

    if problem_info:
        return jsonify(problem_info)
    else:
        return jsonify({"error": "Failed to get hint"}), 500
        
@app.route('/log_event', methods=['POST'])
def log_event(): 
    print(request.json)
    pid = request.json.get('pid')
    sid = request.json.get('sid')
    code = request.json.get('code')
    event_type = request.json.get('event_type')
    event_time = request.json.get('timestamp')
    event_log = request.json.get('event_log')
        # problem_idx, sid: 1, code:code, event_log:event_log, timestamp: Date.now()
    log = Log(sid, pid, code, event_type, event_time, event_log)
    conn = sqlite3.connect("./db/problems_db.sqlite", check_same_thread=False)
    log.write_to_db(conn)
    return jsonify({"status": "success"})

if __name__ == '__main__':
    app.run(debug=True)
