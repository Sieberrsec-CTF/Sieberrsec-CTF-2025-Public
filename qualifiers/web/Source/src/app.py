from flask import Flask, render_template
import os

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/supersecretroute")
def supersecretroute():
    return "Where do web crawlers look to index your page?"

@app.route("/robots.txt")
def robots():
    return os.getenv("FLAG")

if __name__ == "__main__":
    app.run('0.0.0.0', 18537)