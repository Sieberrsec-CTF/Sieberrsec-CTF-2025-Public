from flask import *
import urllib.parse
import os

from bot import admin_bot

app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True

@app.after_request
def apply_csp(response):
    response.headers['Content-Security-Policy'] = "default-src 'self'; script-src 'self'; style-src 'self'; object-src 'none'; base-uri 'none'; frame-ancestors 'none';"
    return response

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

@app.route("/report", methods=["POST"])
def report():
    admin_bot(request.form.get("params"))
    return "ok"

@app.route("/render", methods=["GET"])
def render():
    return render_template("render.html")

@app.route("/upload/<filename>", methods=["POST"])
def upload(filename):

    # sanitize out html
    content = request.form.get("content")
    html_blacklist = ["<", ">", "{", "}"]
    for char in html_blacklist:
        content = content.replace(char, urllib.parse.quote_plus(char))
    content = content.replace("config", "")

    # add the title
    content = "{{title}}" + content

    # remove illegal characters from filename
    filename_blacklist = [".", "/", "\\"]
    filename = list(filename)
    for i, char in enumerate(filename):
        if char in filename_blacklist:
            filename.pop(i)
    
    # one more time, to be safe
    filename = os.path.basename("".join(filename))
    
    # add a file extension if needed
    if not "." in filename:
        filename = filename + ".html"

    with open(f"templates/user_templates/{filename}", "w") as w:
        w.write(content)

    return "ok!"

@app.route("/serve/<filename>", methods=["GET"])
def serve(filename):
    ctx = {"title": f"Serving file: {filename}", **request.args.to_dict()}
    filename = os.path.basename(filename) # no naughty path traversal!
    return render_template(f"user_templates/{filename}", **ctx)

if __name__ == "__main__":
    app.run("0.0.0.0", 38457)