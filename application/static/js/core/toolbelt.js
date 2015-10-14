"use strict";

;(function () {

	var toolbelt = {

		register: function ( name, creator, options ) {

			if (options == null) {
				options = {};
			}

			if ( toolbelt.hasOwnProperty( name ) ) {
				console.warn("We are overwriting the previous action: " + name );
			}

			toolbelt[ name ] = creator;
		}

	};
	
	window.Tools = toolbelt;

})();;

window.Tools.register( "redirect", function ( redirect_url, query_params ) {

	if ( redirect_url === undefined ) {
		window.Tools.redirect( window.location.href );
		return;
	}

	var new_href = redirect_url;

	if ( query_params !== undefined ) {
		new_href += "?" + $.param( query_params );
	}

	window.location.replace( new_href );
});

window.Tools.register( "getCSRF", function () {
	return $('meta[name=csrf-token]').attr("content");
});