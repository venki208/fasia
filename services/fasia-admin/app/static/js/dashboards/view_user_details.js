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

function area_validate(list, help_id, field_name, field_id){
    $("#help_area").html('');
    return new Promise(function (resolve, reject) {
        if(list != null){
            $.ajax({
                method: "POST",
                url: "/auth/check-user-area",
                data:{
                    user_id : user_id,
                    list : list,
                    requested_role: requested_role,
                },
                success: function (response) {
                    if (response.status == true) {
                        $("#"+help_id).html('');
                        $("#"+help_id).html("Already He is admin of "+response.message);
                        $("[name='"+field_id+"']").focus();
                        resolve(true);
                    }
                    else{
                        $("#"+help_id).html('');
                        resolve(false);
                    }
                },
            });
        }
        else{
            $("#help_area").html('');
            $("#help_area").html("Manage Area is Requrired");
            resolve(true);
        }
    });   
}

// attaching on click functionality to submit register button
$("#reg_submit_btn").bind('click', [], register);
// validating registraion form
function validate_registration_form() {
    valid_array = [];
    if (jQuery.inArray(1, valid_array) >= 0) {
        return true;
    } else {
        return false;
    }
}

function register() {
    var params;
    params = {  
        'func_type': 'add',
        'edit_user_id': user_id,
        'user_role' : requested_role,
    };
    if($("#found_mem").prop('checked') == true) {
        params['found_mem'] = $("#found_mem").prop('checked');
    }
    if (requested_role == 'region_admin'){
        params['region_list'] = $('#region').val();
        list = $('#region').val();
        help = "help_region";
        name = "Region";
        id = "region";
    }
    else if(requested_role == 'state_admin'){
        params['state_list'] = $('#state').val();
        list = $('#state').val();
        help = "help_state";
        name = "State";
        id = "state";
    }
    else if(requested_role == 'chapter_admin'){
        params['city_list'] = $('#city').val();
        list = $('#city').val();
        help = "help_city";
        name = "City";
        id = "city";
    }
    
    area_validate(list, help, name, id).then(function(res){
        if(res != true){
            $.ajax({
                method: "POST",
                url: "/auth/admin-dashboard/update-edit-admin-form",
                data:params,
                success: function (response) {
                    if (response.status == 'success') {
                        show_alert(
                            'Success',
                            'edit_admin_details',
                            '<p>Successfully Added.</p>',
                            'href:/auth/admin-dashboard'
                        );
                    }
                },
                error: function (response) {
                    show_alert(
                        'error',
                        'edit_admin_details',
                        '<p>Unable to Update.<br /> Please try again after some time</p>',
                        ''
                    );
                }
            });
        }
    });
}


function get_state(val) {
    $.ajax({
        method: "POST",
        url: '/auth/get-state',
        data: {
            region: $('#region').val()
        },
        success: function (response) {
            if (response.status == true) {
                $("#div_state").css("display", "block");
                $('#state').find('option').remove();
                $('#city').find('option').remove();
                for (var i = 0; i < response.value.length; i++) {
                    $("#state").append('<option value=' + '"' + response.value[i] + '"' + '>' + response.value[i] + '</option>');
                }
                $("#state").multiselect('rebuild')
                $("#state").multiselect({ 
                    maxHeight: 150,
                });
            }
        }
    });
}

function get_city() {
    $.ajax({
        method: "POST",
        url: '/auth/get-city',
        data: {
            state: $('#state').val()
        },
        success: function (response) {
            if (response.status == true) {
                $("#div_city").css("display", "block");
                $('#city').find('option').remove();
                for (var i = 0; i < response.value.length; i++) {
                    $("#city").append('<option value=' + '"' + response.value[i] + '"' + '>' + response.value[i] + '</option>');
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
