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

@application.app.route("/admin/", methods=["GET"])
@tools.adminAuthenticated
def administration( user ):
	
	return render_template("admin/admin.html",
		user=user)

@application.app.route("/admin/neighborhoods/", methods=["GET", "POST"])
@tools.adminAuthenticated
def admin_neighborhoods( user ):

	if request.method == "POST":

		neighborhood = request.form.get("name", "")
		db.admin.addNeighborhood( neighborhood )

		return redirect(url_for("admin_neighborhoods"))

	hoods = db.neighborhoods.getNeighborhoods()

	return render_template("admin/neighborhoods.html",
		user=user,
		hoods=hoods)

@application.app.route("/admin/neighborhoods/create/")
@tools.adminAuthenticated
def admin_create_neighborhood( user ):

	return render_template("admin/create-neighborhood.html",
		user=user)