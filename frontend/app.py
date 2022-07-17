from flask import Flask, render_template, request, session, redirect
import requests
import json
import random
from flask_session import Session
import sqlite3


app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

trashcans_height_cm = {
    # Got these numbers from scouring Amazon, they generally 
    # Are the same weight and width.
    '12 Gallon':  63.5,
    '13 Gallon': 63.5,
    '15 Gallon': 73.6,
    '20 Gallon': 73.7
}

def trashHeightToVolume(height):
    # 44 cm x 33 cm x height
    return 44 *  33 * height

def volumeToWeight(cm3):
    return cm3* (22/84950.5)

prevWeights = [0]*100


@app.route("/")
def root():
    if not session.get('trashcanHeight') or not session.get('trashcan-ip'): return redirect('/config')
    if not session.get('username'): return redirect('/config')
    try:
        value = requests.get(session.get('trashcan-ip'), timeout=2).text
    except:
        return redirect('/config')
    distance = json.loads(value)['distanceCm']
    username = session['username']
    trashcanHeight = session.get('trashcanHeight', 1)
    trashVolume = trashHeightToVolume(max(60 - distance, 0))
    weight = max(volumeToWeight(trashVolume), 0)
    con = sqlite3.connect('users.db')
    cur = con.cursor()
    print(username)
    cur.execute(f"UPDATE Scores SET weight = {weight} WHERE username = '{username}'")
    cur.execute(f"SELECT weight FROM Scores WHERE username = '{username}'")
    con.commit()
    print(cur.fetchall())
    con.close()
    return render_template('index.html', weight=weight)

@app.route("/leaderboard")
def leaderboard():
    if not session.get('trashcanHeight'): return redirect('/config')
    con = sqlite3.connect('users.db')
    cur = con.cursor()
    cur.execute("SELECT username, weight FROM Scores")
    scores = cur.fetchall()
    con.close()
    scores.sort(key=lambda a: a[1])
    return render_template('leaderboard.html', scores=scores)


@app.route("/config", methods=['GET','POST'])
def config():
    if request.method == "POST":
        con = sqlite3.connect('users.db')
        trashcanType = request.form.get('trashcanType')
        username = request.form.get('username')
        ip = request.form.get('ip')
        if (trashcanType not in trashcans_height_cm or not ip) or not username: return redirect('/config')
        session['trashcanHeight'] = trashcans_height_cm.get(trashcanType, 80)
        session['trashcan-ip'] = ip
        session['username'] = username
        cur = con.cursor()
        cur.execute("INSERT OR REPLACE INTO Scores (username, weight) VALUES (?, ?)", (username, 0))
        con.commit()
        con.close()
        return redirect("/")
    return render_template('config.html', trashcanTypes=trashcans_height_cm)


num = random.randint(0, 9999)
@app.route('/refresh')
def refresh():
    return {'state': num}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)