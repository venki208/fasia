var valid_array;

// attaching on click functionality to submit register button
$("#reg_submit_btn").bind('click', [], register);

// attaching datepicker to date of birth
var altFormat = $("#dob").datepicker({
    showAnim: "fold",
    changeMonth: true,
    changeYear: true,
    dateFormat: "dd-mm-yy",
    yearRange: "-100Y:Date()",
    maxDate:'-18Y',
    defaultDate: '-27y',
});

$('#dob').on('keypress', function(e) {
    e.preventDefault(); // Don't allow direct editing
});

$("#home_mobile").intlTelInput({
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

// validating registraion form
function validate_registration_form(){
    valid_array = [];
    valid_array.push(validate_field_onkeypress('title', 'help_title', 'Title'));
    valid_array.push(validate_field_onkeypress('first_name', 'help_first_name', 'First Name'));
    valid_array.push(validate_field_onkeypress('middle_name', 'help_middle_name', 'Middle Name'));
    valid_array.push(validate_field_onkeypress('last_name', 'help_last_name', 'Last Name'));
    valid_array.push(validate_field_onkeypress('dob', 'help_dob', 'Date of Birth'));
    valid_array.push(validate_field_onkeypress('gender', 'help_gender', 'Gender'));
    valid_array.push(validate_field_onkeypress('primary_email', 'help_primary_email', 'Email'));
    valid_array.push(validate_field_onkeypress('home_mobile', 'help_home_mobile', 'Mobile'));
    if (jQuery.inArray(1, valid_array) >= 0){
        return false;
    }else{
        return true;
    }
}
function get_state(val){
    $.ajax({
        method : "POST",
        url : '/auth/get-state',
        data : {
            region : $('#region').val()
        },
        success : function(response){
            if(response.status == true){
                $("#div_state").css("display", "block");
                $('#state').find('option').remove();
                $('#city').find('option').remove();
                for(var i=0; i<response.value.length; i++){
                    $("#state").append('<option value='+'"'+response.value[i]+'"'+'>'+response.value[i]+'</option>');
                }
                $("#state").multiselect('rebuild')
                $("#state").multiselect({ 
                    maxHeight: 150,
                });   
            }
        }
    });
}

function get_city(){
    $.ajax({
        method : "POST",
        url : '/auth/get-city',
        data : {
            state : $('#state').val()
        },
        success : function(response){
            if(response.status == true){
                $("#div_city").css("display", "block");
                $('#city').find('option').remove();
                for(var i=0; i<response.value.length; i++){
                    $("#city").append('<option value='+'"'+response.value[i]+'"'+'>'+response.value[i]+'</option>');
                }
                $("#city").multiselect('rebuild')
                $('#city').multiselect({
                        maxHeight: 150,
                        enableFiltering: true,
                        enableCaseInsensitiveFiltering: true
                });
            }
        }
    });
}

function register(){
    var role = $('#hidden_user_role').val();
    var params = {
        title : $('#title').val(),
        first_name : $('#first_name').val(),
        middle_name: $("#middle_name").val(),
        last_name : $('#last_name').val(),
        gender : $('#gender').val(),
        dob : $('#dob').val(),
        primary_email : $('#primary_email').val(),
        home_mobile : get_mobile_no("#home_mobile"),
        user_role : role,
        profile_pic : $("#id_image_tag").attr('crop-src')
    };

    if (role == 'region_admin'){
        params['region_list'] = $('#region').val();
    }
    else if(role == 'state_admin'){
        params['state_list'] = $('#state').val();
    }
    else if (role == 'chapter_admin'){
        params['city_list'] = $('#city').val();
    }
    if(validate_registration_form()){
        $.ajax({
            method:"POST",
            url:"/auth/add-user/"+role,
            data:params,
            success: function(response){
                if(response.status == true){
                    show_alert(
                        'success',
                        'edit_user_details',
                        '<p>'+response.msg+'</p>',
                        'click:reset_add()'
                    );
                }
            },
            error: function(response){
                show_alert(
                    'error',
                    'edit_user_details',
                    '<p>Unable to Submit/Update.<br /> Please try again after some time</p>',
                    ''
                );
            }
        });
    }
}

function reset_add(){
    $('#reg_form')[0].reset();
    $('#common_modal').modal('hide');
    $('#region').multiselect('refresh');
    $('#state').multiselect('refresh');
    $('#city').multiselect('refresh');
}

// ---------------------------------------------------
// Initialize the Bootstrap Multiselect plugin 
// Refer :http://davidstutz.de/bootstrap-multiselect/ 
// ---------------------------------------------------
$(document).ready(function() {
    $('#region').multiselect({
            maxHeight: 150,
    });
    $('#state').multiselect({
            maxHeight: 150,
            enableFiltering: true,
            enableCaseInsensitiveFiltering: true
    });
    $('#city').multiselect({
            maxHeight: 150,
            enableFiltering: true,
            enableCaseInsensitiveFiltering: true
    });
});