if (user_role_count > 1) {
    show_bootstrap_modal('#ask_role_modal');
} else {
    $(".headline").prepend(fasia_admin_role);
    toogle_admin_creation_divs(selected_user_role);
}
$("button[name='user_role_selection_btn']").on('click', function (e) {
    selected_user_role = this.id;
    var headline = $(this).html();
    $.ajax({
        type: 'POST',
        url:'/auth/set-session',
        data:{
            'key':'selected_role',
            'value': selected_user_role
        },
        success: function(response, xhr, settings){
            if(xhr == 'success'){
                $(".headline").prepend(headline);
                toogle_admin_creation_divs(selected_user_role);
                $("#ask_role_modal").modal('hide');
            }else{
                show_alert(
                    'error',
                    'ask_role_modal',
                    '<p>Unable to process your request \n Please try again after some time.</p>',
                    'reload:true'
                );
            }
        },
        error: function(response){
            show_alert(
                'error',
                'ask_role_modal',
                '<p>Unable to process your request \n Please try again after some time.</p>',
                'reload:true'
            );
        }
    });
});

function toogle_admin_creation_divs(selected_user_role) {
    if(selected_user_role == 'fasia_admin'){
        $(".region_create_admin_btn").toggle();
        $(".state_admin_create_btn").toggle();
        $(".city_admin_create_btn").toggle();
        $(".calender_evnt_div").toggle();
    }
    else if (selected_user_role == 'region_admin') {
        $(".region_create_admin_btn").remove();
        $(".state_admin_create_btn").toggle();
        $(".city_admin_create_btn").toggle();
        $(".calender_evnt_div").remove();
    } else if (selected_user_role == 'state_admin') {
        $(".region_create_admin_btn").parent().remove();
        $(".city_admin_create_btn").toggle();
        $(".state_admin_create_btn").remove();
        $(".calender_evnt_div").remove();
    } else if (selected_user_role == 'chapter_admin') {
        $(".region_create_admin_btn").parent().remove();
        $(".state_admin_create_btn").parent().remove();
        $(".city_admin_create_btn").remove();
        $(".create_user_btn_div").toggle();
        $(".calender_evnt_div").remove();
    }
}