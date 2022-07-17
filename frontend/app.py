from flask import Flask, render_template, request, session, redirect
import requests
import json
import random
from flask_session import Session
import math

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

@app.route("/")
def root():
    print("okie")
    if not session.get('trashcanHeight') or not session.get('trashcan-ip'): return redirect('/config')
    try:
        value = requests.get(session.get('trashcan-ip'), timeout=1).text
    except:
        return redirect('/config')
    print(value)
    distance = json.loads(value)['distanceCm']
    trashcanHeight = session.get('trashcanHeight', 1)
    trashVolume = trashHeightToVolume(max(trashcanHeight - distance, 0))
    weight = volumeToWeight(trashVolume)
    print(value)
    return render_template('index.html', weight=weight)

@app.route("/leaderboard")
def leaderboard():
    if not session.get('trashcanHeight'): return redirect('/config')
    return render_template('leaderboard.html')


@app.route("/config", methods=['GET','POST'])
def config():
    if request.method == "POST":
        trashcanType = request.form.get('trashcanType')
        ip = request.form.get('ip')
        if trashcanType not in trashcans_height_cm or not ip: return redirect('/config')
        session['trashcanHeight'] = trashcans_height_cm.get(trashcanType, 80)
        session['trashcan-ip'] = ip
        return redirect("/")
    return render_template('config.html', trashcanTypes=trashcans_height_cm)


num = random.randint(0, 9999)
@app.route('/refresh')
def refresh():
    return {'state': num}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)