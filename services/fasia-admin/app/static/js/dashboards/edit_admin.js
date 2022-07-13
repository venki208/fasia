var valid_array;
var state_change, state_interval, city_interval;
var upload_img_bnt = $("#admin_upload_btn");
var removable_list = [];
// attaching on click functionality to submit register button
$("#reg_submit_btn").bind('click', [], register);

// attaching datepicker to date of birth
var altFormat = $("#dob").datepicker({
    showAnim: "fold",
    changeMonth: true,
    changeYear: true,
    dateFormat: "dd-mm-yy",
    yearRange: "-100Y:Date()",
    maxDate: '-18Y',
    defaultDate: '-27y',
});


// attaching datepicker to date of birth
var altFormat = $("#dob").datepicker({
    showAnim: "fold",
    changeMonth: true,
    changeYear: true,
    ignoreReadonly: true,
    allowInputToggle: true,
    dateFormat: "dd-mm-yy",
    yearRange: "-100Y:Date()",
    maxDate:'-18Y',
    defaultDate: '-27y',
}).inputmask('dd-mm-yyyy', {
    yearrange: { minyear: (new Date()).getFullYear()-100, maxyear:(new Date()).getFullYear()-18}
});

$('#dob').on('keypress', function (e) {
    e.preventDefault(); // Don't allow direct editing
});

$("#home_mobile").intlTelInput({
    nationalMode: false,
    initialCountry: "auto",
    geoIpLookup: function (callback) {
        $.get('https://ipinfo.io', function () { }, "jsonp").always(function (resp) {
            var countryCode = (resp && resp.country) ? resp.country : "";
            callback(countryCode);
        });
    },
    separateDialCode: true,
});

$("#business_mobile").intlTelInput({
    nationalMode: false,
    initialCountry: "auto",
    geoIpLookup: function (callback) {
        $.get('https://ipinfo.io', function () { }, "jsonp").always(function (resp) {
            var countryCode = (resp && resp.country) ? resp.country : "";
            callback(countryCode);
        });
    },
    separateDialCode: true,
});

set_mobile_no('#home_mobile', home_mobile);
$("#title").val(title);
$("#gender").val(gender);
$("#region")
    .val(region)
    .change();
state_interval = setInterval(function () {
    $("#state")
        .val(home_state)
        .change();
    clearInterval(state_interval);
}, 1000);
city_interval = setInterval(function(){
    $("#city").val(home_city);
    clearInterval(city_interval);
}, 2000);

// validating registraion form
function validate_registration_form() {
    valid_array = [];
    valid_array.push(validate_field_onkeypress('title', 'help_title', 'Title'));
    valid_array.push(validate_field_onkeypress('first_name', 'help_first_name', 'First Name'));
    valid_array.push(validate_field_onkeypress('middle_name', 'help_middle_name', 'Middle Name'));
    valid_array.push(validate_field_onkeypress('last_name', 'help_last_name', 'Last Name'));
    valid_array.push(validate_field_onkeypress('dob', 'help_dob', 'Date of Birth'));
    valid_array.push(validate_field_onkeypress('gender', 'help_gender', 'Gender'));
    valid_array.push(validate_field_onkeypress('region', 'help_region', 'Region'));
    valid_array.push(validate_field_onkeypress('state', 'help_state', 'state'));
    valid_array.push(validate_field_onkeypress('city', 'help_city', 'city'));
    valid_array.push(validate_field_onkeypress('primary_email', 'help_primary_email', 'Email'));
    valid_array.push(validate_field_onkeypress('home_mobile', 'help_home_mobile', 'Mobile'));
    if (jQuery.inArray(1, valid_array) >= 0) {
        return false;
    } else {
        return true;
    }
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

function area_validate(list, help_id, field_name, field_id){
    $("#help_area").html('');
    return new Promise(function (resolve, reject) {
        if(list != null){
            $.ajax({
                method: "POST",
                url: "/auth/check-user-area",
                data:{
                    user_id : edit_user_id,
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
            resolve(false);
        }
    });   
}

function remove_area(id){
    $('#'+id).css("display", "none");
    removable_list.push(id.split('_').join(' '));
}

function register() {
    var params = {
        // Basic
        'func_type': 'edit',
        'edit_user_id': edit_user_id,
        'user_role' : requested_role,
        'membership_type': $("[name='mem_type']:checked").val(),
        'title': $('#title').val(),
        'first_name': $('#first_name').val(),
        'middle_name': $("#middle_name").val(),
        'last_name': $('#last_name').val(),
        'gender': $('#gender').val(),
        'dob': $('#dob').val(),
        'company_name': $('#company').val(),
        'designations': $('#designations').val(),
        'firm_agency_name': $('#firm_agency_name').val(),
        'secondary_email': $('#secondary_email').val(),
        'home_mobile': get_mobile_no("#home_mobile"),
        // Education
        'educational_qualification': $('#educational_qualification').val(),
        'license_number': $('#license_number').val(),
        // Experience
        'products': $('#product').val(),
        'services': $('#services').val(),
        'total_years_practice': $('#total_year').val(),
        'total_client_base': $('#total_client').val(),
        'awards_rewards': $('#award_reward').val(),
        'social_services': $('#socialservice').val(),
        // Home address
        'home_street_address1': $('#home_street_address1').val(),
        'home_street_address2': $('#home_street_address2').val(),
        'home_location': $('#home_location').val(),
        'home_country': $('#home_country').val(),
        'home_state': $('#home_state').val(),
        'home_city': $('#home_city').val(),
        'home_zipcode': $('#home_zipcode').val(),
        'home_phone': $("#home_phone").val(),
        // bussiness address
        'business_street_address1': $('#business_street_address1').val(),
        'business_street_address2': $('#business_street_address2').val(),
        'business_location': $('#business_location').val(),
        'business_country': $('#business_country').val(),
        'business_state': $('#business_state').val(),
        'business_city': $('#business_city').val(),
        'business_zipcode': $('#business_zipcode').val(),
        'business_phone': $('#business_phone').val(),
        'business_mobile': get_mobile_no("#business_mobile"),
        'region': $('#region').val(),
        // profile
        'profile_pic': $("#id_image_tag").attr('crop-src'),
        'communication_email': $("[name='communication_email']:checked").val(),
        'communication_address': $("[name='communication_address']:checked").val(),
    };
    if($("#found_mem").prop('checked') == true) {
        params['found_mem'] = $("#found_mem").prop('checked');
    }
    if (requested_role == 'region_admin'){
        params['region_list'] = $('#region').val();
        list = $('#region').val();
        help = "help_region"
        name = "Region"
        id = "region"
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
        name = "City"
        id = "city"
    }
    if(removable_list.length > 0){
        params['removable_list'] = removable_list;
    }
    area_validate(list, help, name, id).then(function(res){
        if(res != true){
            $.ajax({
                method: "POST",
                url: "/auth/admin-dashboard/update-edit-admin-form",
                data: params,
                success: function (response) {
                    if (response.status == 'success') {
                        show_alert(
                            'success',
                            'edit_admin_details',
                            '<p>Successfully Updated.</p>',
                            'hide:true'
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

// Validating the Zipcode field
function validate_zipcode_form(id, help_id) {
    zipcode_valid_array = [];
    zipcode_valid_array.push(validate_field_onkeypress(id, help_id, 'Zipcode'));
    if (jQuery.inArray(1, zipcode_valid_array) >= 0) {
        return false;
    } else {
        return true;
    }
}

// Function for getting city and state using pincode
function user_city(id, city, state, zip_code) {
    var help_id = $("#" + id).parent().find('.help-block')[0].id;
    if (validate_zipcode_form(id, help_id)) {
        $.ajax({
            method: "POST",
            url: '/auth/admin-dashboard/user-city-update',
            data: {
                zipcode: $('#' + id).val(),
            },
            success: function (response) {
                if (response.status == true) {
                    $("#" + city)
                        .val(response.city)
                        .parent().find('.help-block').html('');
                    $("#" + state)
                        .val(response.state)
                        .parent().find('.help-block').html('');
                    $("#" + zip_code).val($('#' + id).val());
                }
                else if (response.status == false) {
                    $("#" + id).val('');
                    $("#" + help_id).html("Please Enter valid zipcode");
                    $("#" + id).focus();
                }
            }
        });
    }
}

upload_img_bnt.on('click', function(e){
    $('#edit_admin_details').modal('hide');
    $("#imageModal").modal('show');
});

$("#imageModal").on('hidden.bs.modal', function (e) {
    show_bootstrap_modal('#edit_admin_details');
});

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