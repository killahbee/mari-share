from flask import g
from flask import Flask
from flask import request
from flask import session
from flask import jsonify
from flask import url_for
from flask import redirect
from flask import send_file
from flask import render_template

import db
import application
import application.tools as tools

@application.app.route("/dashboard/", methods=["GET"])
@application.app.route("/dashboard/<username>/", methods=["GET"])
@tools.authenticated
def dashboard( user, username=None ):

	if username == None:
		username = user["username"]

	profile_user = db.user.get( username )
	
	return render_template("dashboard/dashboard.html",
		user=user,
		profile_user=profile_user)