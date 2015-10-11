from flask import g
from flask import Flask
from flask import request
from flask import session
from flask import jsonify
from flask import url_for
from flask import send_file
from flask import render_template

from flask_wtf.csrf import CsrfProtect
from flask.ext.bcrypt import Bcrypt

from flask.ext.assets import Environment
from flask.ext.assets import Bundle

import psycopg2.extras
import json
import os

# Define the WSGI application object
app = Flask(__name__)

# Configurations
app.config.from_object('config')

# Define the assets environment
assets = Environment(app)
assets.debug = app.config["DEBUG"]

# Setup the secret key
app.secret_key = app.config["SECRET_KEY"]

# add CSRF protection (http://flask-wtf.readthedocs.org/en/latest/csrf.html)
app.WTF_CSRF_TIME_LIMIT = 86400
csrf_protection = CsrfProtect(app)

# import handlers
import db

# import server.handlers.users

# Define our core bundles
js_core = Bundle('js/core/core.js', filters='rjsmin', output='gen/core.js')
assets.register('js_core', js_core)

css_core = Bundle('css/core/reset.css', filters='scss', output='gen/core.css')
assets.register('css_core', css_core)

# use bcrypt for our passwords
bcrypt = Bcrypt(app)

@app.route("/", methods=["GET"])
def main():
    
    return render_template("main.html")