;(function () {

	"use strict";

	function find_selects ( parent ) {

		if ( parent === undefined ) {
			parent = $("body");
		}

		parent.find("select").each( function ( i , d ) {

			var select = $( d );

			// get the text of the currently selected option
			var initial_text = select.find("[value='" + select.val() + "']").first().text();

			var dom_select = $("<div/>")
				.attr("class", "_select");

			var inner_container = $("<div/>")
				.attr("class", "select-box")
				.appendTo( dom_select );

			$("<i/>")
				.attr("class", "drop-arrow fa fa-sort")
				.appendTo( inner_container );

			var current_value = $("<div/>")
				.attr("class", "current-value truncate")
				.text( initial_text )
				.appendTo( inner_container );

			var dropbox = $("<div/>")
				.attr("class", "drop-box")
				.appendTo( inner_container );

			var options_array = select.find("option, optgroup").map(function ( i, d ) {

				var el = $( d );

				return {
					"type"	: el.prop("tagName").toLowerCase(),
					"value"	: el.attr("value"),
					"text"	: el.text(),
					"label"	: el.attr("label")
				}

			}).toArray();

			options_array.forEach(function ( option ) {

				if ( option.type === "optgroup" ) {
					$("<div/>")
						.attr("class", "option-group")
						.text( option.label )
						.appendTo( dropbox );
				}
				else {
					$("<div/>")
						.attr("class", "select-item")
						.attr("value", option.value )
						.text( option.text )
						.appendTo( dropbox );
				}

			});

			dom_select.insertAfter( select );
			select.hide();

			dom_select.on("click", function (e) {
				e.stopPropagation();
				toggle_menu();
			});

			dropbox.on("click", ".select-item", function () {
				var target = $( this );
				select_item( target.attr("value") );
			});

			function open_menu () {

				// if the drop-box would extend below the current window view, evaluate to true
				var a = ( dom_select.offset().top + dropbox.height() + 50 ) > $(window).height();

				// if the drop-box is taller then the window, evaluate to true
				var b = dropbox.height() > $(window).height();

				// if the drop-box would extend above the nav bar, evaluate to true
				var c = dropbox.height() > ( dom_select.offset().top - 80 );

				// if the drop-box is inside a slideout, evaluate to true
				var d = dom_select.parents("._slideout").length > 0;

				if ( dom_select.hasClass("reverse--drop") ) {
					dom_select.addClass("reverse-drop");
				}
				else if ( a && !b && !c && !d ) {
					dom_select.addClass("reverse-drop");
				}

				dom_select.addClass("show--drop");
			}

			function close_menu () {
				dom_select.removeClass("show--drop");
			}

			function toggle_menu () {
				if ( dom_select.hasClass("show--drop") ) {
					close_menu();
				}
				else {
					open_menu();
				}
			}

			function select_item ( value ) {

				select.val( value );
				current_value.text( select.find("[value='" + value + "']").text() );

				sandbox.notify({
					type: "select-menu-selection",
					data: {
						"action"	: "selected",
						"name"		: select_name,
						"value"		: value
					}
				});
			}

		});

	}

	find_selects();

})();