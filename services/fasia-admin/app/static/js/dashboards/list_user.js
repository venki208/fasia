var confirm_div = $("#confirm_disable_div");
var acpt_dsble_btn = $('#accept_disable_btn');
var sub_dsble_rson = $("#submit_disable_reason");
var title_text;
// function for view the user information
$('#page-content-wrapper').on('click', 'button[name="view_user"]', function(e){
   $.ajax({
        type: 'POST',
        url: '/auth/admin-dashboard/view-user-details',
        data:{
            user_id: $(this).attr('data-id')
        },
        success: function(response){
            $("#list_user_modal_div").html(response);
            show_bootstrap_modal('#view_user_details');
            if(list_type == 'users'){
                $(".admin-data").hide();
                $(".user-data").show();
            }else{
                $(".user-data").hide();
                $(".admin-data").show();
            }
        },
        error: function(response){
            show_alert('error',
                '',
                '<p>Unbale to load User information. <br /> Please try again after some time.</p>',
                ''
            );
        }
   });
});

// function for showing edit form modal
$('#page-content-wrapper').on('click', 'button[name="edit_user"]', function(e){
    var edit_url, modal_id;
    if (list_type == 'admins'){
        edit_url = '/auth/admin-dashboard/edit-admin-details';
        modal_id = '#edit_admin_details';
    }else{
        edit_url = '/auth/admin-dashboard/edit-user-details';
        modal_id = '#edit_user_details';
    }
    $.ajax({
        type: 'POST',
        url: edit_url,
        data:{
            user_id: $(this).attr('data-id'),
            requested_role: requested_role,
        },
        success: function(response){
            $("#list_user_modal_div").html(response);
            show_bootstrap_modal(modal_id);
        },
        error: function(response){
            show_alert('error',
                '',
                '<p>Unbale to edit User information. <br /> Please try again after some time.</p>',
                ''
            );
        }
    });
});

// showing confirmation modal on click of  disable button
$('#page-content-wrapper').on('click', 'button[name="disable_user"]', function(e){
    $("#disable_reason").val('');
    if ($(this).attr('title') == 'Disable User'){
        title_text = 'Disable';
    }else{
        title_text = 'Enable';
    }
    var title_html = 'Do you want to '+title_text+' User';
    $("#question_title").html(title_html);
    show_bootstrap_modal("#confirm_disable_modal");
    // attaching id of user to accept button of conformation modal
    $(acpt_dsble_btn).attr('id', $(this).attr('data-id'));
});

// hiding the confirmation question and showing text area to collect the reason for disable
acpt_dsble_btn.on('click', function(e){
    if (title_text == 'Disable'){
        $("#disable_reason").attr('required', true);
        $("#confirm_disable_div").toggle();
        $("#reason_text_div").toggle();
        $(sub_dsble_rson).attr('id', this.id);
    }else{
        $("#disable_reason").removeAttr('required');
        disable_or_enable_user(this.id);
    }
});

// on cliking of submit button after entering submit reason
sub_dsble_rson.on('click', function(e){
    disable_or_enable_user(this.id);
});

// function for disable the user
function disable_or_enable_user(id){
    if (validate_field_onkeypress('disable_reason', 'help_disable_reason', 'Reason') == 0) {
        $("#help_disable_reason").html('');
        $.ajax({
            type: 'POST',
            url: '/auth/admin-dashboard/disable-or-enable-user',
            data: {
                'user_id': id,
                'disable_reason': $("#disable_reason").val(),
                'title_text': title_text
            },
            success: function (response) {
                if (response.status == 200) {
                    show_alert(
                        'success',
                        'confirm_disable_modal',
                        '<p>User has been ' +title_text+' Successfully</p>',
                        'hide:true'
                    );
                    if(title_text == 'Disable'){
                        $('#disable_'+id)
                        .attr('title', 'Enable User')
                            .find('img')
                            .attr('src', '/auth/static/images/superAdminAssets/fasia_enable_button.png');
                        $('#view_'+id).remove();
                        $('#edit_'+id).remove();
                    }else{
                        var view_dyn_btn = '<button type="button" name="view_user" id="view_'+id+'"'+
                            'class="btn user-action-btn view-user-btn"'+
                            'title="View Details" data-id='+id+'>'+
                                '<img src="/auth/static/images/superAdminAssets/fasia_view_button.png">'+
                            '</button>';
                        var edit_dyn_btn = '<button type="button" name="edit_user" id="edit_'+id+'"'+
                            'class="btn user-action-btn edit-user-btn"'+
                            'title="Edit Details" data-id='+id+'>'+
                                    '<img src = "/auth/static/images/superAdminAssets/fasia_edit_button.png">'+
                            '</button>';
                        $('#disable_'+id).parent().prepend(
                            view_dyn_btn+edit_dyn_btn
                        );
                        $("#disable_" + id)
                            .attr('title', 'Disable User')
                            .find('img')
                            .attr('src', '/auth/static/images/superAdminAssets/fasia_disable_button.png');
                    }
                } else {
                    show_alert(
                        'error',
                        'confirm_disable_modal',
                        '<p>Unable to '+title_text+'.<br /> Please try again after some time.</p>',
                        ''
                    );
                }
            },
            error: function (response) {
                show_alert(
                    'error',
                    'confirm_disable_modal',
                    '<p>Unable to '+title_text+'.<br /> Please try again after some time.</p>',
                    ''
                );
            }
        });
    }
}

// when confirm modal closed resetting values and divs
$("#confirm_disable_modal").on('hidden.bs.modal', function(e){
    $("#confirm_disable_div").css('display', 'block');
    $("#reason_text_div").css('display', 'none');
    $(sub_dsble_rson).attr('id', '');
    $(acpt_dsble_btn).attr('id', '');
});

// Getting Users/Admins List
$(".sidebar-nav a").on('click', function(e){
    $.ajax({
        type: 'POST',
        url: '/auth/list-users/'+req_role_type+'?type='+list_type,
        data:{
            'place_name': $(this).attr('data-content')
        },
        success: function(response){
            $("#page-content-wrapper").html(response);
        },
        error: function(response){
            alert('Unable to Process your request. Please try again after some time');
        }
    });
});

// toggle the active class in side bar list
$(".sidebar-nav li").on('click', function (e) {
    $(".active").removeClass('active');
    $(this).addClass('active');
});

// searching the list of region/state/city and showing list according to search remains hide
function search_sidebar() {
    // Declare variables
    var input, filter, ul, li, a, i;
    input = document.getElementById('serch_li');
    filter = input.value.toUpperCase();
    ul = document.getElementById("myUL");
    li = ul.getElementsByTagName('li');

    // Loop through all list items, and hide those who don't match the search query
    for (i = 0; i < li.length; i++) {
        try {
            a = li[i].getElementsByTagName("a")[0];
            if (a.innerHTML.toUpperCase().indexOf(filter) > -1) {
                li[i].style.display = "";
            } else {
                li[i].style.display = "none";
            }
        } catch (error) {
        }
    }
}