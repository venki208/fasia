var get_advice_btn = $("#advice_button");
get_advice_btn.bind('click', [], get_advice_form_submit);

// Advise mobile number validation with flag
$("#advice_mobile").intlTelInput({
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

set_mobile_no('#advice_mobile', user_mobile);

// validating registraion form
function validate_get_advise_form(){
    var get_advise_array = [];
    get_advise_array.push(validate_field_onkeypress('advice_message', 'help_advice_message', 'Message'));
    get_advise_array.push(validate_field_onkeypress('question_title', 'help_question_title', 'Title'));
    get_advise_array.push(validate_field_onkeypress('advice_mobile', 'help_advice_mobile', 'Mobile Number'));
    get_advise_array.push(validate_field_onkeypress('advice_email', 'help_advice_email', 'Email'));
    get_advise_array.push(validate_field_onkeypress('advice_name', 'help_advice_name', 'Name'));
    if (jQuery.inArray(1, get_advise_array) >= 0){
        return false;
    }else{
        return true;
    }
}

function get_advice_form_submit(){
    if(validate_get_advise_form()){
        $.ajax({
            url: '/advice/get-advice',
            type: 'POST',
            beforeSend: setHeader,
            data: {
                advice_name: $('#get_advice_form').find('#advice_name').val(),
                advice_email: $('#get_advice_form').find('#advice_email').val(),
                advice_mobile: get_mobile_no("input[name='advice_mobile']"),
                advice_title: $("#get_advice_form").find('#question_title').val(),
                advice_message: $('#get_advice_form').find('#advice_message').val(),
                advice_doc_urls: $("[name='advice_doc_urls']").val()
            },
            success: function(response){
                var ok_action, no_btn_action;
                if(response.status == true){
                    var hash = localStorage.getItem("hash");
                    if(hash == "get_advice"){
                        ok_action = 'click:continue_advice();';
                        no_btn_action = '<a class="btn common-model-btn" id="no_button" href="/logout">No</a>';
                    }else{
                        ok_action = 'click:continue_advice();';
                        no_btn_action = '<a class="btn common-model-btn" id="no_button" data-dismiss="modal" aria-hidden="true" onclick="reset_get_advice_form();">No</a>';
                    }
                    show_alert('success',
                        "getAdvisorModal",
                        '<p class="text-center">' + response.value + '</p>' + '<p class="text-center">FASIA team will get back to you within 24 to 48 hrs</p>' +
                        '<p class="text-center">Do you want to continue to seek more advice?</p>',
                        ok_action
                    );
                    $('[name="reset_btn"]').click();
                    $("#uploaded_docs").html('');
                    $("[name='advice_doc_urls']").val('');
                    $("#get_advice_form").find('#question_title').val('');
                    $('#get_advice_form').find('#advice_message').val('');
                    $("#common_btn").html('Yes');
                    $("#common_modal").find(".modal-body").append(no_btn_action);
                }
                else if(response.status == false){
                    show_alert('error',
                        "getAdvisorModal",
                        '<p class="text-center">' + response.value + '</p>',
                        'hide:true'
                    );
                }
            }
        });
    }
}

$('[name="get_advice_form"]').find("[type='text'], textarea").on('keyup keydown change', function(e){
    var field_id = this.id;
    var help_id = $(this).parent().find('.help-block').attr('id');
    var label_name = $(this).attr('placeholder');
    if(field_id == 'advice_mobile'){
        help_id = 'help_advice_mobile';
    } else if (field_id == 'advice_message'){
        label_name = 'Description';
    } else if (field_id == 'question_title'){
        label_name = 'Title';
    }
    validate_field_onkeypress(field_id, help_id, label_name);
});

// resetting the validation messages in form when closing the modal
$("#getAdvisorModal").on('hidden.bs.modal', function (e) {
    var help_tags = $("#get_advice_form").find('.help-block');
    for(i=0; i<help_tags.length; i++){
        $(help_tags[i]).html('');
    }
});

// function will call on select of file for upload
$("#advice_document").on('change', function(e){
    if($(this).val() != ''){
        var up_document = upload_document('upload_doc');
        up_document.success(function(response){
            if(response != 'failed'){
                var doc_urls = $("[name='advice_doc_urls']").val();
                if (doc_urls){
                    doc_urls = doc_urls+","+response;
                    $("[name='advice_doc_urls']").val(doc_urls);
                }else{
                    $("[name='advice_doc_urls']").val(response);
                }
                attach_document('uploaded_docs', response, 'remove_get_advice_doc')
                    .done(hide_show_upload_btn("input[name='advice_doc_urls']", "#paper_clip0"));
            }else{
                alert('Unable to upload the file');
            }
        });
        up_document.error(function(response){
            alert('unable to upload');
        });
    }
});

// function for removing documents
function remove_get_advice_doc(url, event, hidden_input){
    var doc_urls = $("[name='advice_doc_urls']").val();
    var doc_urls_array = doc_urls.split(',');
    for (i=0; i<doc_urls_array.length; i++){
        if(doc_urls_array[i] == url){
            doc_urls_array.splice(i, 1);
        }
    }
    $("[name='advice_doc_urls']").val(doc_urls_array.join());
    $(event).parent().remove();
    hide_show_upload_btn("input[name='advice_doc_urls']", "#paper_clip0");
}

// Showing and hiding the upload icon
function hide_show_upload_btn(elem, button_elem) {
    var docs = $(elem).val();
    var length_docs = docs.split(',').length;
    if (length_docs >= 5) {
        $(button_elem).addClass('hide');
        $(button_elem).parent().append(
            '<h5 id="help_doc_text">You can able to upload upto maximum 5 documents.</h5>'
        );
    } else {
        $(button_elem).removeClass('hide');
        $(button_elem).parent().find('#help_doc_text').remove();
    }
}

// in success modal after submitting the get advice form in question on click of yes button
// function will call
function continue_advice() {
    $("#common_modal").modal('hide');
    $("#fourth_form").fadeOut();
    $("#third_form").fadeIn();
    $("#no_button").remove();
    tab_no = 3; // this tab_no is intialized in get_advice_form.js
    $(".loader").show();
    show_bootstrap_modal('#getAdvisorModal');
    $(".loader").hide();
}

// function will call on click of no button in success modal after submittin the get advice
$("#common_modal").on('click', '#no_button', function(e){
    $('#no_button').remove();
    $("#common_btn").html('Ok');
    $("#first_form").fadeIn();
    $("#third_form").fadeOut();
    $("#fourth_form").fadeOut();
    tab_no = 1;
    reset_get_advice_form();
});

$("#getAdvisorModal").find('.close').on('click', function(e){
    reset_get_advice_form();
});

function show_confirmation_close_advice(){
    show_alert(
        'warning',
        'getAdvisorModal',
        '<p>Do you want to exit?</p>',
        'href:/logout'
    );
    $("#common_btn").html('Yes');
    $("#common_modal").find('.modal-body').append(
        '<a class="btn common-model-btn" onclick="no_close_advice_modal(this);">No</a>'
    );
}

function no_close_advice_modal(btn_no){
    $(btn_no).remove();
    $("#common_btn").html('Ok');
    $("#common_modal").modal('hide');
    $("#getAdvisorModal").modal('show');
}