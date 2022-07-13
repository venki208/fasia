// Intializing the select2 serach bar
$('.js-example-basic-multiple').select2({
    theme: "bootstrap",
    placeholder: 'Search the member',
    minimumInputLength: 3,
    minimumResultsForSearch: 10,
    maximumSelectionLength:1,
    ajax: {
        type: 'POST',
        url: '/auth/admin-dashboard/get_users/'+requested_role,
        data: function(params){
            var query = {
                search_data: params.term,
                page: params.page || 1,
            };
            return query;
        },
        processResults: function (data, params) {
            params.page = params.page || 1;
            var search_result = [];
            search_result = $.map(data.data, function (item) {
                var profile_img;
                if (item.profile_image){
                    profile_img = item.profile_image;
                }else{
                    profile_img = default_icon;
                }
                var fullname = item.first_name+" "+item.middle_name+" "+item.last_name;
                return search_result.concat({
                    'id': item._id.$oid,
                    'text': fullname.replace(" ",""),
                    'icon': profile_img 
                });
            });
            return {
                results: search_result,
                pagination: {
                    more: (params.page * 10) < parseInt(data.total_count)
                }
            };
        },
    },
    cache: true,
    escapeMarkup: function (markup) { return markup; },
    templateResult: formatRepo,
    templateSelection: get_user_information,
});

// making custome dropdown with custome html using response
function formatRepo(repo) {
    if (repo.loading) {
        return repo.text;
    }
    var markup = '<div class="media">' +
            '<div class="media-left media-middle search_icon">'+
                '<a href="#">'+
                    '<img class="media-object" src="'+repo.icon+'" alt="...">'+
                '</a>'+
            '</div>'+
            '<div class="media-body media-middle">'+
                repo.text+        
            '</div>'+
        '</div>';

    if (repo.description) {
        markup += "<div class='select2-result-repository__description'>" + repo.description + "</div>";
    }
    return markup;
}

// calls this function after selection of dropdown and getting respective user information
function get_user_information(repo){
    $.ajax({
        type: 'POST',
        url:'/auth/admin-dashboard/view_details',
        data:{
            user_id: repo.id,
            requested_role:requested_role
        },
        success: function(response){
            $("#user_details_view").html(response);
        },
        error: function(response){
            show_alert('error',
                '',
                '<p>Unable to View the Details of '+ul.item.label+'</p>',
                ''
            );
        }
    });
    return '<span><img src="'+repo.icon+'" class="img-flag" /> ' + repo.text + '</span>';
}