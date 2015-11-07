(function () {
	// handler for the house picture uploader

	"use strict";

	var upload_button = $("#upload-profile-image-button");
	var upload_url = upload_button.attr("data-action");
	var csrftoken = window.Tools.getCSRF();

	var loading;

	var uploader = new ss.SimpleUpload({
		button 				: "upload-profile-image-button",
		url 				: upload_url,
		name 				: "uploadfile",
		responseType		: "json",
		// noParams			: true,
		multipart			: true,
		allowedExtensions	: ['jpg', 'jpeg', 'png', 'gif', 'svg'],
		customHeaders		: { "X-CSRFToken": csrftoken },
		hoverClass			: "hover-state",

		onSubmit: function ( filename, extension ) {
			// gets called BEFORE the file is uploaded

			// loading = window.Core.notifications.loading();
			upload_button.removeClass("loading success error");
			upload_button.addClass("loading");
		},

		onComplete: function ( filename, response, btn, file_element ) {

			// loading.close();
			upload_button.removeClass("loading");
			upload_button.addClass("success");

			// if ( response.status === 200 ) {
			// 	window.Core.notifications.success();
			// }

		},

		onError: function ( filename, errorType, status, statusText, response, btn, file_element ) {
			// error occured

			// loading.close();
			upload_button.removeClass("loading");
			window.Core.notifications.error();
		}
	});
	
})();

(function () {
	// handler for the house picture uploader

	"use strict";

	var upload_button = $("#upload-cover-image-button");
	var upload_url = upload_button.attr("data-action");
	var csrftoken = window.Tools.getCSRF();

	var loading;

	var uploader = new ss.SimpleUpload({
		button 				: "upload-cover-image-button",
		url 				: upload_url,
		name 				: "uploadfile",
		responseType		: "json",
		// noParams			: true,
		multipart			: true,
		allowedExtensions	: ['jpg', 'jpeg', 'png', 'gif', 'svg'],
		customHeaders		: { "X-CSRFToken": csrftoken },
		hoverClass			: "hover-state",

		onSubmit: function ( filename, extension ) {
			// gets called BEFORE the file is uploaded

			// loading = window.Core.notifications.loading();
			upload_button.removeClass("loading success error");
			upload_button.addClass("loading");
		},

		onComplete: function ( filename, response, btn, file_element ) {

			upload_button.removeClass("loading");
			upload_button.addClass("success");

			// loading.close();

			// if ( response.status === 200 ) {
			// 	window.Core.notifications.success();
			// }

		},

		onError: function ( filename, errorType, status, statusText, response, btn, file_element ) {
			// error occured

			// loading.close();
			upload_button.removeClass("loading");
			window.Core.notifications.error();
		}
	});
	
})();