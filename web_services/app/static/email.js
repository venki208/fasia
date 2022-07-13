var contact_form_submit = $("#contact_us_form_btn");

$("#mobile").intlTelInput({
    nationalMode: false,
    initialCountry: "auto",
	geoIpLookup: function(callback) {
	    $.get('https://ipinfo.io', function() {}, "jsonp").always(function(resp) {
	        var countryCode = (resp && resp.country) ? resp.country : "";
	        callback(countryCode);
	    });
	},
    separateDialCode: true,
});

$("#name, #contact_email, #mobile, #message").on('keyup keydown',function() {
	var field_name = $(this).attr('placeholder');  
	var help_id = $(this).closest(".form-group").find('.help-block')[0].id;
	var is_valid = validate_field_onkeypress(this.id, help_id, field_name);
});

function validate_contact_us_form(){
	var is_message = validate_field_onkeypress("message", "help_message", 'Message');
	var is_mobile = validate_field_onkeypress("mobile", "help_mobile", "Mobile");
	var is_email = validate_field_onkeypress("contact_email", "help_email", "Your Email");
	var is_name = validate_field_onkeypress("name", "help_name", "Your Name");
	if(is_name !=0 || is_email != 0 || is_mobile != 0 || is_message != 0){
        return false;
    }else{
        return true;
    }
}


contact_form_submit.on('click', function(e){
	var is_valid = validate_contact_us_form();
	if(is_valid){
		$.ajax({
			method: "POST",
			url: '/contact_us',
			beforeSend: setHeader,
			data:{
				'name' : $("input[name='name']").val(),
				'email': $("input[name='email']").val(),
				'mobile': get_mobile_no("input[name='mobile']"),
				'message': $("[name='message']").val()
			},
			success: function(response){
				if(response == 'success'){
					$("[name='reset_form']").click();
					$("#sendmessage").fadeIn();
					$("#sendmessage").fadeOut(5000,"swing");
				}
			},
			error: function(response){
				alert('Unable to send email \n Please try again after some time');
			}
		});
	}
});