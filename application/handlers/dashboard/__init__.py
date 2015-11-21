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

	is_logged_in_user = False

	if username == None:
		username = user["username"]

	if username == user["username"]:
		is_logged_in_user = True

	profile_user = db.user.get( username )

	if is_logged_in_user:
		messages = db.messages.get( userid=profile_user["userid"] )
	else:
		messages = []
	
	return render_template("dashboard/dashboard.html",
		user=user,
		messages=messages,
		profile_user=profile_user,
		is_logged_in_user=is_logged_in_user)

@application.app.route("/messages/<username>/", methods=["GET", "POST"])
@tools.authenticated
def send_message( user, username=None ):

	if username == None:
		abort(404)

	profile_user = db.user.get( username )

	if request.method == "GET":
		
		return render_template("dashboard/create-message.html",
			user=user,
			profile_user=profile_user)

	elif request.method == "POST":

		message = request.form.get("message", None)
		errors = []

		message_success = db.messages.send(
			subject=profile_user["userid"],
			author=user["userid"],
			message=message
		)

		if message_success:
			return redirect(url_for("dashboard", username=username))

		errors.append("Couldn't create message.")

		return render_template("dashboard/create-message.html",
			user=user,
			message=message,
			profile_user=profile_user)