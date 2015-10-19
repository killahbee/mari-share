from flask import g
from flask import Flask
from flask import request
from flask import session
from flask import jsonify
from flask import url_for
from flask import redirect
from flask import send_file
from flask import render_template

import application
import application.tools as tools

@application.app.route("/dashboard/", methods=["GET"])
@tools.dbauthenticated
def dashboard( user ):
    
    return render_template("dashboard/dashboard.html",
    	user=user)