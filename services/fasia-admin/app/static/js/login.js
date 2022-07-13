var login_btn = $("#login_button");
login_btn.bind('click', [], login_user); // binding login user function as click event

// Removing cookie value
localStorage.removeItem('selected_user_role'); 

function validate_login_form(){
    var is_login_captcha = validate_recptcha(login_captcha, 'help_login_recpatcha');
    var is_password = validate_field_onkeypress('password', 'help_admin_pwd', 'Password');
    var is_username = validate_field_onkeypress('username', 'help_admin_username', 'Email Id');
    if(is_username == 1 || is_password == 1|| is_login_captcha == false){
        return false;
    }else{
        return true;
    }
}

// make user login
function login_user(){
    if(validate_login_form()){
        $.ajax({
            url: '/auth/login',
            type: 'POST',
            data: {
                username: $('#login_form').find('#username').val(),
                password: $('#login_form').find('#password').val(),
            },
            success: function(response){
                if(response.status == true){
                    $("#help_login_validation").html('');
                    window.location.href = response.next;
                }
                else if(response.status == 'blocked'){
                    $("#help_login_validation").html('Your Account is blocked. Please contact to our adminstrator');
                }
                else {
                    $("#help_login_validation").html('Invalid User Email ID / Password');
                }
            },
            error: function(response){
                show_alert(
                    'error',
                    '',
                    '<p>Unable to Process Login <br /> Please try again after some time</p>',
                    'hide:true'
                );
            }
        });
    }
}