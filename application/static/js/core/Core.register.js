(function () {

	"use strict";

	var root = this;
	var _registered_actions = [];

	var core = {

		register	: function ( name, action, options ) {

			if ( core.hasOwnProperty( name ) ) {
				console.warn("We are overwriting the previous action: " + name );
			}

			core[ name ] = action;
			_registered_actions.push( name );
		}

	};

	// make it public
	root.Core = core;

}.call(this));