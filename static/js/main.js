
    $(document).ready(function($) {
        $('#popup-login-open').click(function () {
            $('#popup-login').fadeIn();
            return false;
        });
    });

	$(document).ready(function ($) {
        $('#popup-register-open').click(function() {
		    $('#popup-register').fadeIn();
		return false;
	});

	$('.popup-close').click(function() {
		$(this).parents('.popup-fade').fadeOut();
		return false;
	});

	$(document).keydown(function(e) {
		if (e.keyCode === 27) {
			e.stopPropagation();
			$('.popup-fade').fadeOut();
		}
	});

	$('.popup-open').click(function(e) {
		if ($(e.target).closest('.popup').length === 0) {
			$(this).fadeOut();
		}
	});
});