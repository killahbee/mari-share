;(function () {

	"use strict";

	var coreModal = {};

	coreModal.create = function ( modal_options ) {

		var parent = $("<section/>");

		var modal_html = "<div class='modal-container'>";
		modal_html += "<div class='modal'>";
		modal_html += "<div class='modal-content'>";

		// icon
		if ( modal_options.hasOwnProperty("icon") ) {
			modal_html += "<div class='modal-icon " + modal_options["icon"] + "'></div>";
		}

		// title
		if ( modal_options.hasOwnProperty("title") ) {
			modal_html += "<h2>" + modal_options["title"] + "</h2>";
		}

		// description
		if ( modal_options.hasOwnProperty("description") ) {
			modal_html += "<p>" + modal_options["description"] + "</p>";
		}

		// form elements
		if ( modal_options.hasOwnProperty("form") ) {
			modal_html += modal_options["form"]
			// modal_html += "<label>Email</label>";
			// modal_html += "<input type='text' name='email'>";
			// modal_html += "<label>Username</label>";
			// modal_html += "<input type='text' name='username'>";
			// modal_html += "<label>Password</label>";
			// modal_html += "<input type='password' name='password'>";
		}

		// close modal-content
		modal_html += "</div>";

		// close modal
		modal_html += "<div class='close-modal fa fa-times'></div>";

		// modal buttons
		modal_html += "<div class='modal-foot'>";
		modal_html += "<button class='button blue'>" + modal_options["ok-button"] + "</button>";
		modal_html += "</div>";

		// close modal and modal-container
		modal_html += "</div>";
		modal_html += "</div>";

		parent.html( modal_html );

	}

	return;

	create({
		"icon"			: "fa fa-leaf",
		"title"			: "Let's do this!",
		"description"	: "Network with the people that can take you high places.",
		"form"			: "<label>Email</label><input type='text' name='email'><label>Username</label><input type='text' name='username'><label>Password</label><input type='password' name='password'>",
		"ok-button"		: "Continue"
	})

})();