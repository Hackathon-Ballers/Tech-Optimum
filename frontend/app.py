from flask import Flask, render_template
import random

app = Flask(__name__)

@app.route("/")
def root():
    return render_template('index.html')


num = random.randint(0, 9999)
@app.route('/refresh')
def refresh():
    return {'state': num}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)