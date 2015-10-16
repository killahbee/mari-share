import os
import re

from functools import wraps

from flask import g
from flask import abort
from flask import url_for
from flask import session
from flask import request
from flask import redirect

import requests

import db

def authenticated(fn):

	@wraps(fn)
	def _wrap(*args, **kwargs):

		if "email" not in session:
			return redirect(url_for('login', next=request.url))
			
		user_object = {
			"userid"	: session["userid"],
			"email"		: session["email"],
			"username"	: session["username"]
		}

		return fn(user=user_object, *args, **kwargs)
	return _wrap

def dbauthenticated(fn):

	@wraps(fn)
	def _wrap(*args, **kwargs):

		if "email" not in session:
			return redirect(url_for('login', next=request.url))

		user_object = db.user.get( session["userid"] )

		return fn(user=user_object, *args, **kwargs)
	return _wrap

def setCookie ( email=None, username=None, userid=None ):

	if email == None or username == None or userid == None:
		return False

	session['email'] = email
	session['username'] = username
	session["userid"] = userid

	return True