import json
import os

from flask import Flask, redirect, request
from flask_basicauth import BasicAuth

from urllib.parse import urlparse

def is_absolute(url):
    return bool(urlparse(url).netloc)

config_file_path = os.environ.get('CONFIG_FILE_PATH', 'config.json')
app = Flask(__name__)
port = os.environ.get('PORT', '8080')
app.config['BASIC_AUTH_USERNAME'] = os.environ.get('BASIC_AUTH_USERNAME', 'admin')
app.config['BASIC_AUTH_PASSWORD'] = os.environ.get('BASIC_AUTH_PASSWORD', 'admin')
basic_auth = BasicAuth(app)

@app.route('/app/<appname>' , methods=['GET'])
def get(appname):
    redirects = app.config["REDIRECTS"]

    if appname not in redirects:
        return f"App {appname} not found"

    app_config = redirects[appname]
    last_redir_url = app_config["redirections"][-1]["url"]
    return redirect(last_redir_url)

@app.route('/config', methods=['GET'])
@basic_auth.required
def getConfig():
    redirects = app.config["REDIRECTS"]
    return {
        "success": True,
        "config": redirects
    }

@app.route('/app/<appname>', methods=['POST', 'PUT'])
@basic_auth.required
def set(appname):
    posted_json = request.get_json()
    if posted_json is None:
        return {"success": False, "error": "Please provide a json object"}
    if "url" not in posted_json:
        return {"success": False, "error": "No url provided, please provide a json object with a 'url' key"}
    if not is_absolute(posted_json["url"]):
        return {"success": False, "error": "Please provide an absolute url"}

    try:
        app_config = app.config["REDIRECTS"][appname]
    except KeyError:
        app_config = {
            "redirections": []
        }
        app.config["REDIRECTS"][appname] = app_config

    app_config["redirections"].append(
        {
            "url": posted_json["url"]
        }
    )

    with open(config_file_path, "w") as f:
        json.dump(app.config["REDIRECTS"], f)

    return {"success": True, "app": app_config}


if __name__ == '__main__':
    try:
        with open(config_file_path, "r") as f:
            app.config["REDIRECTS"] = json.load(f)
    except FileNotFoundError:
        app.config["REDIRECTS"] = {}

    app.run(debug=False, port=port, host="0.0.0.0")
