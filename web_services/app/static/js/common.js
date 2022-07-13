var get_adv_btn_shake;
// function for getting the mobile number with country code
function get_mobile_no(widget){
    var mobile = $(widget).intlTelInput("getNumber").trim().replace(/\s+/g, "");
    return mobile;
}

// function for setting the mobile number with country code
function set_mobile_no(widget, value){
    $(widget).intlTelInput("setNumber", value);
}

// showing bootstrap modal
function show_bootstrap_modal(elem){
    $(elem).modal({
        show:true,
        backdrop: 'static',
        keyboard: false
    });
}

// function for setting success/error/alert information to common modal is showing
function show_alert(type_msg, old_modal_id, data, btn_type){
    var msg = '';
    if(old_modal_id){
        $("#"+old_modal_id).modal('hide');
    }
    switch(type_msg){
        case "success":
            msg = "<i class='fa fa-check success'></i>";
            break;
        case "warning":
            msg = "<i class='glyphicon glyphicon-warning-sign warning'></i>";
            break;
        case "error":
            msg = "<i class='glyphicon glyphicon-remove-circle error'></i>";
            break;
    }
    $("#common_modal").find("#msg_type").html(msg);
    $("#common_modal").find(".sub-div").empty();
    $("#common_modal").find(".sub-div").append(data);
    // removing the old attr except type and class attr
    if(btn_type){
        $("#common_btn").css('display', 'inline-block');
        var old_attr = $("#common_btn")[0].getAttributeNames();
        $.each(old_attr, function(e){
            if(old_attr[e] != 'type' && old_attr[e] != 'class' && old_attr[e] !='id'){
                $("#common_btn").removeAttr(old_attr[e]);
            }
        });
        var type_fun = btn_type.split(':');
        switch(type_fun[0]){
            case 'click':
                $('#common_btn').attr('onclick', type_fun[1]);
                break;
            case 'hide':
                $("#common_btn")
                    .attr('data-dismiss', "modal")
                    .attr('aria-hidden',"true");
                break;
            case 'href':
                $("#common_btn").attr('href', type_fun[1]);
                break;
            case 'reload':
                $("#common_btn").attr('onclick', 'return window.location.reload();');
                break;
        }
    }else{
        $("#common_btn").css('display', 'none');
    }
    $("#common_modal").modal('show');
}

// function for setting csrf token as header
function setHeader(xhr, settings){
    if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type) && !this.crossDomain) {
        xhr.setRequestHeader("X-CSRFToken", csrf_token);
    }
    $(".loader").show();
}

// Binding the loading event ot whole document
// set global : false in ajax request for not load this script
$(document).ajaxStart(function () {
});
$(document).ajaxStop(function () {
    $(".loader").hide();
});
function hide_modal(){
    $("#common_modal").modal('hide');
}

// function for shake the button
jQuery.fn.shake = function (intShakes, intDistance, intDuration) {
    this.each(function () {
        $(this).css("position", "relative");
        for (var x = 1; x <= intShakes; x++) {
            $(this).animate({ left: (intDistance * -1) }, (((intDuration / intShakes) / 4)))
                .animate({ left: intDistance }, ((intDuration / intShakes) / 2))
                .animate({ left: 0 }, (((intDuration / intShakes) / 4)));
        }
    });
    return this;
};

// on foucs of window get advice button will shake
$(window).focus(function () {
    if (!get_adv_btn_shake){
        get_adv_btn_shake = setInterval(function () {
            $(".getAdv-btn").shake(3, 7, 800);
        }, 5000);
    }
});
// focus out of window shake effect will reset to null
$(window).blur(function () {
    clearInterval(get_adv_btn_shake);
    get_adv_btn_shake = 0;
});

function show_more_sm(){
    $("#sm-more").toggle();
    if($("#show_more").find('i').hasClass('fa-sort-desc')){
        $("#show_more").html(
            '<i class="fa fa-sort-asc"></i>'
        );
    }else{
        $("#show_more").html(
            '<i class="fa fa-sort-desc"></i>'
        );
    }
}