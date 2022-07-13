var valid_array;

// attaching on click functionality to submit register button
$("#reg_submit_btn").bind('click', [], register);

// attaching datepicker to date of birth
var altFormat = $("#dob").datepicker({
    showAnim: "fold",
    changeMonth: true,
    changeYear: true,
    ignoreReadonly: true,
    allowInputToggle: true,
    dateFormat: "dd-mm-yy",
    yearRange: "-100Y:Date()",
    maxDate: '-18Y',
    defaultDate: '-27y',
});

$('#dob').on('keypress', function (e) {
    e.preventDefault(); // Don't allow direct editing
});

// setting values to input tags
$("#title").val(title);
$("#gender").val(gender);
if (communication_email == 'secondary') {
    $("#yes_secondary").prop('checked', true);
}
if (communication_address == 'business') {
    $("#id_business_address").prop('checked', true);
}
// attching value to membership type radio buttons
var memship_input_tags = $("#mem_type_div").find('input[name="mem_type"]');
for (i = 0; i < memship_input_tags.length; i++) {
    if (memship_input_tags[i].value == membership_type) {
        $(memship_input_tags[i]).prop('checked', true);
    }
}

if (found_member == 'True'){
    $("[name='foun_type'").prop('checked', true);
}else{
    $("[name='foun_type'").prop('checked', false);
}

// attaching mobile to input tag
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
set_mobile_no('#business_mobile', bussiness_mobile);

// validating the registration form onkey up or keydown
$("#reg_form").find("[type='text'], select, [type='date'], textarea").on('keyup keydown change', function (e) {
    var field_id = this.id;
    var help_id = $(this).parent().find('.help-block').attr('id');
    var label_name = $(this).parent().find('label').html();
    if (label_name != '' || label_name != undefined) {
        if (field_id != 'home_mobile' && field_id != 'business_mobile' && field_id != 'city_search') {
            if (label_name.indexOf('*') >= 0) {
                label_name = label_name.replace('*', "");
            }
        } else {
            label_name = '';
        }
    }
    if (field_id == 'home_mobile') {
        help_id = 'help_home_mobile';
        label_name = 'Mobile Number';
    } else if (field_id == 'business_mobile') {
        help_id = 'help_business_mobile';
        label_name = 'Mobile Number';
    }
    validate_field_onkeypress(field_id, help_id, label_name);
});

$("[name='communication_email']").on('change', function (e) {
    var communication_email_type = $(this).val();
    if (communication_email_type == 'secondary') {
        $("#secondary_email")
            .attr('required', 'true');
    } else {
        $("#secondary_email")
            .removeAttr('required');
    }
});

$("[name='address_type']").on('change', function (e) {
    var cummunication_address_type = $(this).val();
    var business_inputs = $("#business_information_div").find('input.form-control');
    var span_help_tags = $("#business_information_div").find('span.help-block');
    for (i = 0; i < business_inputs.length; i++) {
        if (cummunication_address_type == 'business' && business_inputs[i].id != 'business_phone') {
            $(business_inputs[i]).attr('required', 'true');
        } else {
            $(business_inputs[i]).removeAttr('required');
            $(span_help_tags[i]).html('');
        }
    }
});


// validating registraion form
function validate_registration_form() {
    valid_array = [];
    valid_array.push(validate_field_onkeypress('business_mobile', 'help_business_mobile', 'Mobile Number'));
    valid_array.push(validate_field_onkeypress('home_phone', 'help_home_phone', 'Phone Number'));
    valid_array.push(validate_field_onkeypress('business_zipcode', 'help_business_zipcode', 'Zipcode'));
    valid_array.push(validate_field_onkeypress('business_city', 'help_business_city', 'City'));
    valid_array.push(validate_field_onkeypress('business_state', 'help_business_state', 'State'));
    valid_array.push(validate_field_onkeypress('business_country', 'help_business_country', 'Country'));
    valid_array.push(validate_field_onkeypress('business_location', 'help_business_location', 'Location'));
    valid_array.push(validate_field_onkeypress('business_street_address2', 'help_business_street_address2', 'Street Address2'));
    valid_array.push(validate_field_onkeypress('business_street_address1', 'help_business_street_address1', 'Street Address1'));
    valid_array.push(validate_field_onkeypress('home_mobile', 'help_home_mobile', 'Mobile Number'));
    valid_array.push(validate_field_onkeypress('home_phone', 'help_home_phone', 'Phone Number'));
    valid_array.push(validate_field_onkeypress('home_zipcode', 'help_home_zipcode', 'Zipcode'));
    valid_array.push(validate_field_onkeypress('home_city', 'help_home_city', 'City'));
    valid_array.push(validate_field_onkeypress('home_state', 'help_home_state', 'State'));
    valid_array.push(validate_field_onkeypress('home_country', 'help_home_country', 'Country'));
    valid_array.push(validate_field_onkeypress('home_location', 'help_home_location', 'Location'));
    valid_array.push(validate_field_onkeypress('home_street_address2', 'help_home_street_address2', 'Street Address2'));
    valid_array.push(validate_field_onkeypress('home_street_address1', 'help_home_street_address1', 'Street Address1'));
    valid_array.push(validate_radio_fields('address_type', 'help_address_type', 'Address Type'));
    valid_array.push(validate_field_onkeypress('socialservice', 'help_socialservice', 'Social Service'));
    valid_array.push(validate_field_onkeypress('award_reward', 'help_award_reward', 'Awards and Reward'));
    valid_array.push(validate_field_onkeypress('total_client', 'help_total_client', 'Total client Base'));
    valid_array.push(validate_field_onkeypress('total_year', 'help_total_year', 'Total Years of Practice'));
    valid_array.push(validate_field_onkeypress('services', 'help_services', 'Services'));
    valid_array.push(validate_field_onkeypress('product', 'help_product', 'Product'));
    valid_array.push(validate_field_onkeypress('license_number', 'help_license_number', 'License Information'));
    valid_array.push(validate_field_onkeypress('educational_qualification', 'help_educational_qualification', 'Educational Qualification'));
    valid_array.push(validate_field_onkeypress('firm_agency_name', 'help_firm_agency_name', 'Firm / Agency_name'));
    valid_array.push(validate_field_onkeypress('designations', 'help_designations', 'Designation'));
    valid_array.push(validate_field_onkeypress('fasia_designation', 'help_fasia_designation', 'Fasia Designation'));
    valid_array.push(validate_field_onkeypress('secondary_email', 'help_secondary_email', 'Secondary Email'));
    valid_array.push(validate_field_onkeypress('company', 'help_company', 'Company'));
    valid_array.push(validate_field_onkeypress('dob', 'help_dob', 'Date of Birth'));
    valid_array.push(validate_field_onkeypress('gender', 'help_gender', 'Gender'));
    valid_array.push(validate_field_onkeypress('last_name', 'help_last_name', 'Last Name'));
    valid_array.push(validate_field_onkeypress('middle_name', 'help_middle_name', 'Middle Name'));
    valid_array.push(validate_field_onkeypress('first_name', 'help_first_name', 'First Name'));
    valid_array.push(validate_field_onkeypress('title', 'help_title', 'Title'));
    valid_array.push(validate_radio_fields('mem_type', 'help_mem_type', 'Membership Type'));
    if (jQuery.inArray(1, valid_array) >= 0) {
        return false;
    } else {
        return true;
    }
}

function register() {
    if (validate_registration_form()) {
        $.ajax({
            method: "POST",
            url: "/auth/admin-dashboard/update-edit-user-form",
            data: {
                user_id: user_id,
                membership_type: $("[name='mem_type']:checked").val(),
                found_mem: $("[name='foun_type']").prop('checked'),
                secondary_email: $('#secondary_email').val(),
                gender: $('#gender').val(),
                dob: $('#dob').val(),
                first_name: $('#first_name').val(),
                middle_name: $("#middle_name").val(),
                last_name: $('#last_name').val(),
                designations: $('#designations').val(),
                fasia_designation: $('#fasia_designation').val(),
                title: $('#title').val(),
                company_name: $('#company').val(),
                firm_agency_name: $('#firm_agency_name').val(),
                educational_qualification: $('#educational_qualification').val(),
                license_number: $('#license_number').val(),
                home_email: $('#home_email').val(),
                home_street_address1: $('#home_street_address1').val(),
                home_street_address2: $('#home_street_address2').val(),
                home_location: $('#home_location').val(),
                home_country: $('#home_country').val(),
                home_state: $('#home_state').val(),
                home_city: $('#home_city').val(),
                home_zipcode: $('#home_zipcode').val(),
                home_phone: $("#home_phone").val(),
                home_mobile: get_mobile_no("#home_mobile"),
                products: $('#product').val(),
                services: $('#services').val(),
                total_years_practice: $('#total_year').val(),
                total_client_base: $('#total_client').val(),
                awards_rewards: $('#award_reward').val(),
                social_services: $('#socialservice').val(),
                business_street_address1: $('#business_street_address1').val(),
                business_street_address2: $('#business_street_address2').val(),
                business_location: $('#business_location').val(),
                business_country: $('#business_country').val(),
                business_state: $('#business_state').val(),
                business_city: $('#business_city').val(),
                business_zipcode: $('#business_zipcode').val(),
                business_phone: $('#business_phone').val(),
                business_mobile: get_mobile_no("#business_mobile"),
                send_email_to: $('#send_email_to').val(),
                primary_email: $('#primary_email').val(),
                communication_email: $("[name='communication_email']:checked").val(),
                communication_address: $("[name='communication_address']:checked").val(),
            },
            success: function (response, xhr, settings) {
                if (settings.getResponseHeader('Content-Type') == 'text/html; charset=utf-8') {
                    $("#registration_dynamic_modal_div").html(response);
                    show_bootstrap_modal('#sms_otp_modal');
                } else {
                    if (response.status == true) {
                        var res_msg;
                        if (is_registered == 'True') {
                            res_msg = 'You have updated the registration form successfully.';
                        } else {
                            res_msg = 'You have completed the registration successfully, Please check your mail for login credentials.';
                        }
                        show_alert('success',
                            "edit_user_details",
                            '<p class="text-center">' + res_msg + '</p>',
                            'hide:true'
                        );
                    }
                    else if (response.status == false) {
                        show_alert('error',
                            "edit_user_details",
                            '<p class="text-center">' +
                            'Unable to update the Registration form.<br /> Please Try again after some time.</p>'
                        );
                    }
                }
            },
            error: function (response) {
                show_alert('error',
                    "edit_user_details",
                    '<p class="text-center">' +
                    'Unable to update the Registration form.<br /> Please Try again after some time.</p>'
                );
            }
        });
    }
}

$("[name='mem_type']").on('change', function (e) {
    if ($(this).val() != "")
        $('#help_mem_type').html('');
});

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
