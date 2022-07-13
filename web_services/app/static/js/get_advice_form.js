var tab_no = 1;
var next_step;
var ask_advice_mob, ask_advice_email;


$('.get-advice-registration-form fieldset:first-child').fadeIn('slow');

$('.get-advice-registration-form input[type="text"], .get-advice-registration-form textarea').on('focus', function () {
    $(this).removeClass('input-error');
});

// validating the first step
function validate_first_step(){
    var first_form_array = [];
    first_form_array.push(validate_field_onkeypress('advice_name', 'help_advice_name', 'Name'));
    first_form_array.push(validate_field_onkeypress('advice_email', 'help_advice_email', 'Email'));
    first_form_array.push(validate_field_onkeypress('advice_mobile', 'help_advice_mobile', 'Mobile'));
    if (jQuery.inArray(1, first_form_array) >= 0) {
        return false;
    } else {
        return true;
    }
}

// validating the third step
function validate_third_step(){
    var third_step_array = [];
    third_step_array.push(validate_field_onkeypress('question_title','help_question_title','Title'));
    third_step_array.push(validate_field_onkeypress('advice_message','help_advice_message','Message/Purpose'));
    if (jQuery.inArray(1, first_form_array) >= 0) {
        return false;
    } else {
        return true;
    }
}

// next step
$('.get-advice-registration-form .btn-next').on('click', function () {
    var parent_fieldset = $(this).parents('fieldset');
    var next_step = true;

    parent_fieldset.find('input[type="text"], textarea').each(function () {
        if ($(this).val() == "") {
            $(this).addClass('input-error');
            next_step = false;
        }
        else {
            var help_id;
            if (this.id == 'advice_mobile'){
                help_id = 'help_advice_mobile';
            }else{
                help_id = $(this).parent().find('.help-block')[0].id;
            }
            var label = $(this).attr('placeholder').replace('*','');
            if (validate_field_onkeypress(this.id, help_id, label) == 1){
                next_step = false;
            }
            else{
                $(this).removeClass('input-error');
            }
        }
    });

    if (next_step) {
        if($(parent_fieldset).attr('id') == 'first_form'){
            ask_advice_mob = get_mobile_no("input[name='advice_mobile']");
            ask_advice_email = $("#advice_email").val();
            $.ajax({
                method: 'POST',
                url: '/advice/send-ask-advice-otp',
                beforeSend: setHeader,
                data: {
                    name: $("#advice_name").val(),
                    email: ask_advice_email,
                    mobile_num: ask_advice_mob
                },
                success: function (res) {
                    if(res.status == 200){
                        parent_fieldset.fadeOut(400, function (e) {
                            tab_no = tab_no + 1;
                            if (tab_no == 4) {
                                $("#fourth_form").fadeIn();
                            } else {
                                $(this).next().fadeIn();
                            }
                        });
                    }else{
                        alert('unable to send otp');    
                    }
                },
                error: function (res) {
                    alert('unable to send otp');
                }
            });
        }
        else if ($(parent_fieldset).attr('id') == 'second_form') {
            var validation_result = validate_ask_advice_otp();
            validation_result.success(function (e, textStatus, xhr){
                if (xhr.status == 200) {
                    if (e.mobile_otp && e.email_otp){
                        if (e.verifed == true && e.validate == false) {
                            var validation_otp_result = validate_ask_advice_otp({
                                mobile_otp: $("#get_ad_mob_otp").val(),
                                email_otp: $("#get_ad_email_otp").val(),
                                'mobile_num': ask_advice_mob,
                                'email_id': ask_advice_email,
                                validate: true
                            });
                            validation_otp_result.success(function(e, textStatus, xhr){
                                if(xhr.status == 200){
                                    if(e.mobile_otp && e.email_otp && e.verifed && e.validate){
                                        parent_fieldset.fadeOut(400, function (e) {
                                            tab_no = tab_no + 1;
                                            if (tab_no == 4) {
                                                $("#fourth_form").fadeIn();
                                            } else {
                                                $(this).next().fadeIn();
                                            }
                                        });
                                    }
                                }
                            });
                        }
                    }else{
                        if(!e.mobile_otp){
                            $("#help_get_ad_mob_otp").html('Please enter valid mobile OTP');
                        }else{
                            $("#help_get_ad_mob_otp").html('');
                        }
                        if(!e.email_otp){
                            $("#help_get_ad_email_otp").html('Please enter valid email OTP');
                        }else{
                            $("#help_get_ad_email_otp").html('');
                        }
                    }
                } else {
                    $("#help_get_ad_mob_otp").html('Please enter valid mobile OTP');
                    $("#help_get_ad_email_otp").html('Please enter valid email OTP');
                }
            });
            validation_result.error(function(res) {
                is_otp_fields_completed = false;
            });
        }
        else {
            parent_fieldset.fadeOut(400, function (e) {
                tab_no = tab_no + 1;
                if(tab_no == 4){
                    $("#fourth_form").fadeIn();
                }else{
                    $(this).next().fadeIn();
                }
            });
        }
    }

});

// previous step
$('.get-advice-registration-form .btn-previous').on('click', function () {
    $(this).parents('fieldset').fadeOut(400, function () {
        if(tab_no == 4){
            $("#third_form").fadeIn();
        }else if(tab_no == 3){
            $("#first_form").fadeIn();
            tab_no = tab_no - 1;
        }
        else{
            $(this).prev().fadeIn();
        }
        tab_no = tab_no - 1;
    });
});

// submit
$('.get-advice-registration-form').on('submit', function (e) {
    $(this).find('input[type="text"], textarea').each(function () {
        if ($(this).val() == "") {
            e.preventDefault();
            $(this).addClass('input-error');
        }
        else {
            $(this).removeClass('input-error');
        }
    });
});

// Validating and verifying the OTP
function validate_ask_advice_otp(data_obj){
    var otp_data_obj;
    if (!data_obj){
        otp_data_obj = {
            mobile_otp: $("#get_ad_mob_otp").val(),
            email_otp: $("#get_ad_email_otp").val(),
            'mobile_num': ask_advice_mob,
            'email_id': ask_advice_email
        };
    }else{
        otp_data_obj = data_obj;
    }
    return $.ajax({
        method: 'POST',
        url: '/advice/verify-ask-adv-otp',
        beforeSend: setHeader,
        data: otp_data_obj,
    });
}

function reset_get_advice_form(){
    $("#first_form").fadeIn();
    $("#second_form").fadeOut();
    $("#third_form").fadeOut();
    $("#fourth_form").fadeOut();
    tab_no = 1;
    set_mobile_no("input[name='advice_mobile']", user_mobile);
    $('#get_advice_form').find('#advice_name').val(user_first_name);
    $('#get_advice_form').find('#advice_email').val(user_email);
    $("#get_advice_form").find('#question_title').val('');
    $('#get_advice_form').find('#advice_message').val('');
    $("[name='advice_doc_urls']").val('');
    $("#uploaded_docs").html('');
}