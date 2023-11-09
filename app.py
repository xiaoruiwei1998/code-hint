from flask import Flask, render_template, request, jsonify
import requests
import sys
import subprocess
import openai
from models.hint import Hint
from models.problem import Problem

input_data = """
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

output_data = "{'#dance': 9, '#viral': 8, '#trending': 3, '#party': 2, '#hiphop': 2, '#duet': 2, '#moves': 2, '#street': 2, '#classic': 2, '#latin': 2, '#salsa': 2, '#beats': 2, '#electro': 1, '#swing': 1, '#fun': 1, '#summer': 1, '#challenge': 1, '#ballet': 1, '#dreams': 1, '#elegance': 1, '#streetdance': 1, '#revolution': 1, '#freestyle': 1, '#vibes': 1, '#fiesta': 1, '#hit': 1, '#groove': 1, '#night': 1, '#retro': 1, '#oldies': 1, '#throwback': 1, '#tapdance': 1, '#tunes': 1, '#rhythm': 1, '#tap': 1, '#urban': 1, '#citylife': 1, '#bollywood': 1, '#bash': 1, '#indian': 1, '#festive': 1, '#colorful': 1}"

example_user_prompt = """file_path = 'coding_problems/tiktok/top10videos.csv'
hashtag_count = {}
import csv
csvfile_path = 'coding_problems/icecream_menu.csv'
with open(csvfile_path, 'r') as file:  # open file
    reader = csv.reader(file) # read file 
    data = list(reader) # store data to a list 
    print(data) # print data to debug"""

example_feedback = """worked_example:
        for row in data: # data is a 2-d list, each item in data is an 1-d list
            print(row) # see the structure of each row
            col_0 = row[0] # get the value on (row_0, col_0)"""
            

app = Flask(__name__)

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
    hint = Hint(problem_desc=problem_desc, code=code, input_data=input_data, output_data=output_data, example_user_prompt=example_user_prompt, example_feedback=example_feedback)
    print(hint)
    response = hint.generateGPTAnswer()
    if response:
        return jsonify(hints = response)
    else:
        return jsonify({"error": "Failed to get hint"}), 500
    
@app.route('/get_problem', methods=['POST'])
def get_problem():
    problem_idx = request.json.get('idx')
    problem = Problem()
    problem_info = problem.get_problem()
    if problem_info:
        return jsonify(problem_info)
    else:
        return jsonify({"error": "Failed to get hint"}), 500
        

if __name__ == '__main__':
    app.run(debug=True)
