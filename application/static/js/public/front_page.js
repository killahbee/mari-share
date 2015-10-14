;(function () {

	"use strict";

	var modal_html = "";
	modal_html += "<label>Email</label>";
	modal_html += "<input type='text' name='email'>";
	modal_html += "<label>Username</label>";
	modal_html += "<input type='text' name='username'>";
	modal_html += "<label>Password</label>";
	modal_html += "<input type='password' name='password'>";

	$("#js-free-account-button").on("click", function () {

		Core.modal.create({
			"icon"			: "fa fa-leaf",
			"title"			: "Let's do this!",
			"description"	: "Network with the people that can take you high places.",
			"form"			: modal_html,
			"form-method"	: "POST",
			"form-action"	: "/signup/",
			"ok-button"		: "Continue"
		});

	});

})();