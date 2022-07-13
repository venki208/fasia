reset_pwd_submit_btn = $('button[name="reset_submit_btn"]');

$("[type='password']").on('keyup keydown change', function(e){
    var field_name;
    var field_id = this.id;
    var help_id = $(this).parent().find('.help-block').attr('id');
    if(field_id == 'new_pwd'){
        field_name = 'New Password';
    }else{
        field_name = 'Confirm Password';
    }
    validate_field_onkeypress(field_id, help_id, field_name);
});

function validate_reset_pwd_form(){
    var new_pwd = $("#new_pwd").val();
    var conf_pwd = $("#conf_pwd").val();
    var missed_field = 0;
    var is_conf_pwd = validate_field_onkeypress('conf_pwd', 'help_conf_pwd', 'Confirm Password');
    var is_new_pwd = validate_field_onkeypress('new_pwd', 'help_new_pwd', 'New Password');
    if (new_pwd != conf_pwd){
        $("#help_conf_pwd").html('New password and confirm password should be same');
        missed_field = 1;
    }
    if(is_conf_pwd !=0 || is_new_pwd != 0){
        missed_field = 1;
    }
    if(missed_field == 0){
        return true;
    }else{
        return false;
    }
}

reset_pwd_submit_btn.on('click', function(e){
    if (validate_reset_pwd_form() == true){
        $.ajax({
            method: 'POST',
            url: '/auth/reset_pwd/'+activation_key,
            data:{
                'new_pwd' : $("#new_pwd").val(),
                'conf_pwd' : $("#conf_pwd").val()
            },
            success: function(response){
                if(response.status == 200){
                    show_alert('success',
                        "",
                        '<p class="text-center">' +
                        'You have reset the password successfully!</p>',
                        'href:/auth'
                    );
                }else{
                    show_alert('error',
                        "",
                        '<p class="text-center">' +
                        'Unbale to reset password. Please try again after sometime</p>'
                    );
                }
            },
            error: function(response){
                show_alert('error',
                    "",
                    '<p class="text-center">' +
                    'Unbale to reset password. Please try again after sometime</p>'
                );
            }
        });
    }
});