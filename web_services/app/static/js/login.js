var forget_pwd_link = $("#forget_pwd_link");
var forget_sub_btn = $("#submit_forget_pwd");
var forget_pwd_form = $("#forget_form");

$("[name='get_advice_login_button']").on('click', function(e){
    $("#login_form_div").hide();
    $("#loginModalLabel").hide();
    $("#fb_btn").attr('disabled', true);
    $("#google_btn").attr('disabled', true);
    $("#linkedin_btn").attr('disabled', true);
    $("#loginModal").find(".tit").empty();
    $("#loginModal").find(".tit").append(
        '<p class="text-left">This is purely a recommendation based on the data and the information provided by you. Please consult registered and regulated financial advisors before making your decisions. FASIA is only a facilitated of connecting advisor with you. FASIA is not responsible for any recommendation/advices provided by any one in this platform.</p>'+
        '<div class="checkbox" name="get_advice_soc_div">'+
            '<label>'+
                '<input type="checkbox" name="get_advice_soc_check" id="get_advice_soc_check"> By clicking you are accepting Terms & Conditions of Fasiaamerica.org.'+
            '</label>'+
        '</div>'
    );
    location.hash = "get_advice";
});

$("#get_modal_login_button").on('click', function(e){
    $("#login_form_div").show();
    $("#loginModalLabel").show();
    $("#loginModal").find(".tit").empty();
    $("#loginModal").find(".tit").append("<p>Don't have an account? Sign up through</p>");
    location.hash = "";
});

var login_btn = $("#login_button");
login_btn.bind('click', [], login_user); // binding login user function as click event

function validate_login_form(){
    var is_login_captcha = validate_recptcha(login_captcha, 'help_login_recpatcha');
    var is_password = validate_field_onkeypress('password', 'help_password', 'Password');
    var is_username = validate_field_onkeypress('username', 'help_username', 'Email Id');
    if(is_username == 1 || is_password == 1 || is_login_captcha == false){
        return false;
    }else{
        return true;
    }
}

// make user login
function login_user(){
    if(validate_login_form()){
        $.ajax({
            url: '/login',
            type: 'POST',
            beforeSend: setHeader,
            data: {
                username: $('#login_form').find('#username').val(),
                password: $('#login_form').find('#password').val(),
            },
            success: function(response){
                if(response.status == true){
                    $("#help_login_validation").html('');
                    window.location.href = next_url;
                }
                else if(response.status == 'blocked'){
                    show_alert('warning',
                        "loginModal",
                        '<p class="text-center">' +
                        'Your account is blocked Please contact to our adminstrator.</p>'
                    );
                }
                else {
                    $("#help_login_validation").html('Invalid User Email ID / Password');
                }
            },
            error: function (response) {
                show_alert('error',
                    "loginModal",
                    '<p class="text-center">' +
                    'Unable to Process Your request \n Please try again after some time.</p>'
                );
            }
        });
    }
}

function navigate_user(response){
    if(response.status == true){
        localStorage.setItem("hash", response.hash);
        window.location.href = '/';
    }else if(response.status == 'not_active'){
        show_alert('warning',
            "loginModal",
            '<p class="text-center">' +
            'Your account is blocked Please contact to our adminstrator.</p>'
        );
    }else{
        show_alert('error',
            "loginModal",
            '<p class="text-center">' +
            'Unable to Process Your request \n Please try again after some time.</p>'
        );
    }
}

// Hiding and empty the div of alert in login modal
$('#loginModal').on('hidden.bs.modal', function (e) {
    forget_pwd_form.addClass('hide');
});

// forget password block ----------------------------
forget_pwd_link.on('click', function(e){
    forget_pwd_form.toggleClass('hide');
    $("#forget_email").focus();
});

// validatin email and sending the reset password link
forget_sub_btn.on('click', function(e){
    if(validate_field_onkeypress('forget_email', 'help_forget_email', 'Email ID') == 0 
        && validate_recptcha(forgot_pwd_captcha, 'help_forgot_recpatcha') == true){
        $.ajax({
            method: 'POST',
            url: '/forget_pwd',
            beforeSend: setHeader,
            data:{
                'email' : $("#forget_email").val()             
            },
            success: function(res){
                if(res.status == 200){
                    if(res.disabled == false){
                        if(res.is_reg == true){
                            show_alert('success',
                                "loginModal", 
                                '<p class="text-center">'+
                                    'Please check your email to reset the password.</p>',
                                'hide:"hide_modal()"'
                            );
                        }else{
                            $("#help_forget_email").html('You are not registered');
                        }
                    }else{
                        show_alert('warning',
                            "loginModal",
                            '<p class="text-center">' +
                            'Your account is blocked Please contact to our adminstrator.</p>'
                        );
                    }
                }else{
                    $("#help_forget_email").html('Not found in our system. <br /> Please provide registered Email');
                }
            },
            error: function(response){
                show_alert('error',
                    "loginModal",
                    '<p class="text-center">' +
                    'Unable to Process Your request \n Please try again after some time.</p>'
                );
            }
        });
    }
});

// show/hide the password
$('.pwd-add-on').on('click', function(e){
    var icon;
    if ($("#password").attr('type') == 'password'){
        icon = '<i class="fa fa-eye-slash"></i>';
        $('#password').attr('type', 'text');
    }else{
        icon = '<i class="fa fa-eye"></i>';
        $('#password').attr('type', 'password');
    }
    $(this).html(icon);
});

$('#loginModal').on('change', '[name="get_advice_soc_check"]', function(e){
    var advice_accept = $('[name="get_advice_soc_check"]').prop('checked');
    if (advice_accept){
        $("#fb_btn").removeAttr('disabled');
        $("#google_btn").removeAttr('disabled');
        $("#linkedin_btn").removeAttr('disabled');
    }else{
        $("#fb_btn").attr('disabled', true);
        $("#google_btn").attr('disabled', true);
        $("#linkedin_btn").attr('disabled', true);
    }
});

$("#get_modal_login_button").on('click', function(e){
    $("#fb_btn").removeAttr('disabled');
    $("#google_btn").removeAttr('disabled');
    $("#linkedin_btn").removeAttr('disabled');
});