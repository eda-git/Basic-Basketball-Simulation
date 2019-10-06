from flask import Flask, render_template, request
import sys
# Imports dbGet and tipOff from game.py
from game import dbGet, tipOff

app = Flask(__name__)


@app.route('/',methods=['GET', 'POST'])
def index():
    context = {
        "title": 'Home',
    }
    return render_template('index.html', content = context)

@app.route('/about',methods=['GET', 'POST'])
def about():
    context = {
        "title": 'About',
    }
    return render_template('about.html', content = context)


@app.route('/gameplay',methods=['GET', 'POST'])
def gameplay():
    teamOne = dbGet(request.args.get("away"))
    teamTwo = dbGet(request.args.get("home"))
    # Converts get(games) into int 
    Games = int(request.args.get("games"))
    context = tipOff(teamOne, teamTwo, Games)
    return render_template('gameplay.html', content = context)


