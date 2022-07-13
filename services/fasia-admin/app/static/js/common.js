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
function show_alert(type_msg, old_modal_id, data, btn_type) {
    var msg = '';
    if (old_modal_id) {
        $("#" + old_modal_id).modal('hide');
    }
    switch (type_msg) {
        case "success":
            msg = "<i class='far fa-check-circle success'></i>";
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
    if (btn_type) {
        $("#common_btn").css('display', 'inline-block');
        var old_attr = $("#common_btn")[0].getAttributeNames();
        $.each(old_attr, function (e) {
            if (old_attr[e] != 'type' && old_attr[e] != 'class' && old_attr[e] != 'id') {
                $("#common_btn").removeAttr(old_attr[e]);
            }
        });
        var type_fun = btn_type.split(':');
        switch (type_fun[0]) {
            case 'click':
                $('#common_btn').attr('onclick', type_fun[1]);
                $("#common_modal").find('.close').attr('onclick', type_fun[1]);
                break;
            case 'hide':
                $("#common_btn")
                    .attr('data-dismiss', "modal")
                    .attr('aria-hidden', "true");
                break;
            case 'href':
                $("#common_btn").attr('href', type_fun[1]);
                $("#common_modal").find('.close').attr('href', type_fun[1]);
                break;
            case 'reload':
                $("#common_btn").attr('onclick', 'return window.location.reload();');
                $("#common_modal").find('.close').attr('onclick', 'return window.location.reload();');
                break;
        }
    } else {
        $("#common_btn").css('display', 'none');
        $("#common_modal").find('.close').removeAttr('onclick');
    }
    $("#common_modal").modal('show');
}