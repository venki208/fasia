function validate_field_onkeypress(field_id, help_id, field_name){
    var is_max_length = $("#"+field_id).attr("max-length");
    var is_min_length = $("#"+field_id).attr("min-length");
    var is_required = $("#"+field_id).attr("required");
    var is_email = $("#"+field_id).attr("is-email");
    var is_number = $("#"+field_id).attr("is-num");
    var is_mobile = $("#"+field_id).attr("is-mobile");
    var is_text = $("#"+field_id).attr("is-text");
    var is_pwd = $("#"+field_id).attr("pwd-pattern");
    var is_select = $("#"+field_id).attr("is-select");
    var missed_field = 0;
    var v_m = '';

    if(missed_field == 0){
        $("#"+field_id).removeClass('not_valid');
        $("#"+help_id).html('');
        missed_field = 0;
    }
    if(is_max_length){
        if (is_max_length < $("#"+field_id).val().length){
            if(is_number){
                v_m = ' numbers';
            }else{
                v_m = ' characters';
            }
            $("#"+help_id).html('Please enter less than '+is_max_length+v_m);
            $("#"+field_id).addClass("not_valid");
            $("#"+field_id).focus();
            missed_field = 1;
        }
    }
    if(is_min_length){
        if(is_min_length > $("#"+field_id).val().length
            && $("#"+field_id).val() != ''){
            if(is_number){
                v_m = ' numbers';
            }else{
                v_m = ' characters';
            }
            $("#"+help_id).html('Please enter minimum '+is_min_length+v_m);
            $("#"+field_id).addClass("not_valid");
            $("#"+field_id).focus();
            missed_field = 1;
        }
    }
    if(is_number){
        var re = /^[0-9]*$/;
        if(!re.test($("#"+field_id).val())){
            $("#"+help_id).html('Please enter only numbers');
            $("#"+field_id).addClass("not_valid");
            $("#"+field_id).focus();
            missed_field = 1;
        }
    }
    if(is_text){
        var text_re = /^[a-zA-Z ]+$/;
        if(!text_re.test($("#"+field_id).val()) && $.trim($("#"+field_id).val()) != ''){
            $("#"+help_id).html('Please enter only characters');
            $("#"+field_id).addClass("not_valid");
            $("#"+field_id).focus();
            missed_field = 1;
        }
    }
    if(is_pwd){
        var pwd_pattern = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[$@$!%*#?&])[A-Za-z\d$@$!%*#?&]{8,}$/;
        if(!pwd_pattern.test($("#"+field_id).val())){
            $("#"+help_id).html('Please enter valid password');
            $("#"+field_id).addClass("not_valid");
            $("#"+field_id).focus();
            missed_field = 1;
        }
    }
    if(is_required){
        if($("#"+field_id).val() == ''){
            var field_type;
            if(is_select){
                field_type = 'Select';
            }else{
                field_type = 'Please enter';
            }
            $("#"+help_id).html(field_type+' '+field_name);
            $("#"+field_id).addClass("not_valid");
            $("#"+field_id).focus();
            missed_field = 1;
        }
    }
    if(is_email && $.trim($("#"+field_id).val()) != ''){
        var re_email = /^([\w-]+(?:\.[\w-]+)*)@((?:[\w-]+\.)*\w[\w-]{0,66})\.([a-z]{2,6}(?:\.[a-z]{2})?)$/i;
        if (!re_email.test($("#"+field_id).val())){
            $("#"+help_id).html('Please enter valid Email ID');
            $("#"+field_id).addClass("not_valid");
            $("#"+field_id).focus();
            missed_field = 1;
        }
    }
    if(is_mobile && $.trim($("#"+field_id).val()) != ''){
        var isValidNumber = $('#'+field_id).intlTelInput("isValidNumber");
        if (!isValidNumber) {
            $("#"+help_id).html('Please enter valid Mobile Number');
            $("#"+field_id).addClass("not_valid");
            $("#"+field_id).focus();
            missed_field = 1;
        }
    }
    return missed_field;
}

function validate_radio_fields(field_id, help_id, field_name){
    var missed_field = 0;
    if($("[name='"+field_id+"']:checked").length <= 0){
        $("#"+help_id).html('Please select '+field_name);
        missed_field = 1;
        $("[name='"+field_id+"']").focus();
    }
    return missed_field;
}

// validating the recaptcha
function validate_recptcha(widget_id, help_id) {
    var is_recaptcha = grecaptcha.getResponse(widget_id);
    if (is_recaptcha) {
        $("#" + help_id).html('');
        $("#" + help_id).removeClass('recaptcha-help-block');
        return true;
    } else {
        $("#" + help_id).addClass('recaptcha-help-block');
        $("#" + help_id).html('Please Complete the Recaptcha');
        return false;
    }
}