from flask import g
from flask import Flask
from flask import request
from flask import session
from flask import jsonify
from flask import url_for
from flask import send_file
from flask import render_template

import db
import application
import application.tools as tools

@application.app.route("/directory/", methods=["GET"])
@tools.authenticated
def directory( user ):

	users = db.user.get()
	
	return render_template("directory/directory.html",
		users=users)