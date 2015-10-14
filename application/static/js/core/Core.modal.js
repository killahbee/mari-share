;(function () {

	"use strict";

	var root = this;
	var coreModal = {};
	var _body = $("body");

	coreModal.create = function ( modal_options ) {

		var parent = $("<section/>")
			.attr("class", "curtain")

		var modal_html = "<div class='modal-container'>";
		modal_html += "<div class='modal'>";

		if ( modal_options.hasOwnProperty("form") ) {
			modal_html += "<form method='" + modal_options["form-method"] + "' action='" + modal_options["form-action"] + "'>"
		}

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
		}

		// close modal-content
		modal_html += "</div>";

		// close modal
		modal_html += "<div class='close-modal fa fa-times'></div>";

		// modal buttons
		modal_html += "<div class='modal-foot'>";
		modal_html += "<button class='button blue'>" + modal_options["ok-button"] + "</button>";
		modal_html += "</div>";

		if ( modal_options.hasOwnProperty("form") ) {
			modal_html += "</form>"
		}

		// close modal and modal-container
		modal_html += "</div>";
		modal_html += "</div>";

		parent.html( modal_html );

		if ( modal_options.hasOwnProperty("form") ) {
			$("<input/>")
				.attr("type", "hidden")
				.attr("name", "_csrf_token")
				.val( window.Tools.getCSRF() )
				.appendTo( parent.find("form") );
		}

		parent.on("click", ".close-modal", function () {
			parent.remove();
		});

		setTimeout(function () {
			parent.find(".modal").addClass("show");
		}, 200);

		_body.append( parent );

	}

	root.Core.register("modal", coreModal);

}.call(this));