from flask import Flask, render_template
import requests
import json
import random
from flask_session import Session

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

def trashcanHeightToVolume(height):
    # 44 cm x 33 cm x height
    return 588.9498 * height

def volumeToWeight(cm3):
    return cm3* (22/91.44)

@app.route("/")
def root():
    value = requests.get("http://192.168.1.223").text
    distance = json.loads(value)['distanceCm']
    print(value)
    return render_template('index.html', dist=distance)

@app.route("/leaderboard")
def leaderboard():
    return render_template('leaderboard.html')

num = random.randint(0, 9999)
@app.route('/refresh')
def refresh():
    return {'state': num}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)