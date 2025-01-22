from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/sql-injection")
def sql():
    return render_template('sql-injection.html')

@app.route("/found-me")
def found():
    return render_template('found.html')

@app.route("/decode-me")
def decode():
    return render_template('decode.html')

app.run()