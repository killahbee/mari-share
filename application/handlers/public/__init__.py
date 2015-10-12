from flask import g
from flask import Flask
from flask import request
from flask import session
from flask import jsonify
from flask import url_for
from flask import send_file
from flask import render_template

import application

@application.app.route("/", methods=["GET"])
def main():
    
    return render_template("public/front_page.html")