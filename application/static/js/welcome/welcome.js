(function () {
	// handler for the house picture uploader

	"use strict";

	var upload_button = $("#js-upload-avatar-image-button");
	var upload_url = upload_button.attr("data-action");
	var loading;

	var uploader = new ss.SimpleUpload({
		button 				: "js-upload-avatar-image-button",
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

			loading = window.Core.notification.loading();
		},

		onComplete: function ( filename, response, upload_button, file_element ) {

			loading.close();

			console.log( response );

			if( response.errors.length > 0 ) {
				Core.notification.notification("error", response.errors);
			}
			else {
				if ( response.status == 200 ) {
					Core.notification.notification("success");
				}
			}

			if ( response.hasOwnProperty("data") && response.data.hasOwnProperty("imageid") ) {
				add_image_to_list( response.data.imageid );
			}
		},

		onError: function ( filename, errorType, status, statusText, response, upload_button, file_element ) {
			// error occured

			loading.close();

			console.log( status );
			console.log( response );

			if ( status === 413 ) {
				Core.notification.notification("error", "Image can't exceed 8MB.");
			}
			else {
				Core.notification.notification("error");
			}
		}
	});

	function add_image_to_list ( imageid ) {
		$("<img/>")
			.attr("class", "house-image")
			.attr("src", "/image/" + imageid + "/")
			.appendTo( $("#js-image-list") );
	}
	
})();