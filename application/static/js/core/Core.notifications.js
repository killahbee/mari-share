;(function () {

	"use strict";

	var root = this;
	var coreNotifications = {};
	var _body = $("body");

	coreNotifications.loading = function () {

		var parent = $("<div/>")
			.attr("class", "application-loading");

		$("<img/>")
			.attr("src", "/static/img/spinners/puff.svg")
			.appendTo( parent );

		_body.append( parent );

		return {

			"spinner"	: parent,

			close: function () {
				parent.remove();
			}
		}

	};

	coreNotifications.success = function () {

		var parent = $("<div/>")
			.attr("class", "application-success");

		$("<i/>")
			.attr("class", "fa fa-check")
			.appendTo( parent );

		_body.append( parent );

		setTimeout(function () {
			parent.remove();
		}, 1500);

		return {

			"element"	: parent,

			close: function () {
				parent.remove();
			}
		}

	};

	coreNotifications.error = function () {

		var parent = $("<div/>")
			.attr("class", "application-error");

		$("<i/>")
			.attr("class", "fa fa-times")
			.appendTo( parent );

		_body.append( parent );

		setTimeout(function () {
			parent.remove();
		}, 1500);

		return {

			"element"	: parent,

			close: function () {
				parent.remove();
			}
		}

	};

	root.Core.register("notifications", coreNotifications);

}.call(this));