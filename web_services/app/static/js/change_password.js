var change_pwd_submit_btn = $("button[name='change_submit_btn']");
var old_pwd_field = $("#old_pwd");
var new_pwd_field = $("#new_pwd");
var conf_pwd_field = $("#conf_pwd");
$("[type='password']").on('keyup keydown change', function (e) {
    var field_name;
    var field_id = this.id;
    var help_id = $(this).parent().find('.help-block').attr('id');
    if (field_id == 'new_pwd') {
        field_name = 'New Password';
    }else if (field_id == 'old_pwd'){
        field_name = 'Old Password';
    }else {
        field_name = 'Confirm Password';
    }
    validate_field_onkeypress(field_id, help_id, field_name);
});

function validate_change_pwd_form() {
    var old_pwd = old_pwd_field.val();
    var new_pwd = new_pwd_field.val();
    var conf_pwd = conf_pwd_field.val();
    var missed_field = 0;
    var is_conf_pwd = validate_field_onkeypress('conf_pwd', 'help_conf_pwd', 'Confirm Password');
    var is_new_pwd = validate_field_onkeypress('new_pwd', 'help_new_pwd', 'New Password');
    var is_old_pwd = validate_field_onkeypress('old_pwd', 'help_old_pwd', 'Old Password');
    if (new_pwd != conf_pwd) {
        $("#help_conf_pwd").html('New password and confirm password should be same');
        missed_field = 1;
    }
    if (is_conf_pwd != 0 || is_new_pwd != 0 || is_old_pwd != 0) {
        missed_field = 1;
    }
    if (missed_field == 0) {
        return true;
    } else {
        return false;
    }
}

change_pwd_submit_btn.on('click', function(e){
    if(validate_change_pwd_form() == true){
        $.ajax({
            type: 'POST',
            beforeSend: setHeader,
            url: '/change_password',
            data: {
                'old_pwd' : old_pwd_field.val(),
                'new_pwd' : new_pwd_field.val(),
                'conf_pwd': conf_pwd_field.val(),
            },
            success: function (data, statusText, xhr){
                if(xhr.status == 200){
                    show_alert('success',
                        "",
                        '<p class="text-center">' +
                        'You have changed the password successfully. <br />'+
                        'Click Ok to login again</p>',
                        'href:/logout'
                    );
                }else if(xhr.status == 304){
                    $("#help_old_pwd").html('Please enter correct password');
                }else{
                    show_alert(
                        'error',
                        '',
                        '<p>Unable Change the password right now. <br /> Please try again after some time</p>',
                        ''
                    );
                }
            },
            error: function(response){
                show_alert(
                    'error',
                    '',
                    '<p>Unable Change the password right now. <br /> Please try again after some time</p>',
                    ''
                );
            }
        });
    }
});