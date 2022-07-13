function launch_upwrdz_app() {
    $.ajax({
        type: 'POST',
        url: '/launch_upwrdz',
        beforeSend: setHeader,
        success: function (response_dict) {
            if (response_dict.status) {
                var x = document.getElementById("form_div");
                var createform = document.createElement('form');
                createform.setAttribute("action", url);
                createform.setAttribute("method", "POST");
                createform.setAttribute("class", "form_name");
                createform.setAttribute("id", "form_id");
                x.appendChild(createform);

                var inputelement = document.createElement('input');
                inputelement.setAttribute("type", "text");
                inputelement.setAttribute("name", "token");
                inputelement.setAttribute("value", response_dict.token);
                createform.appendChild(inputelement);

                var input_username = document.createElement('input');
                input_username.setAttribute("type", "text");
                input_username.setAttribute("name", "username");
                input_username.setAttribute("value", response_dict.username);
                createform.appendChild(input_username);

                var input_user_role = document.createElement('input');
                input_user_role.setAttribute("type", "text");
                input_user_role.setAttribute("name", "users_role");
                input_user_role.setAttribute("value", response_dict.users_role);
                createform.appendChild(input_user_role);

                var input_user_first_name = document.createElement('input');
                input_user_first_name.setAttribute("type", "text");
                input_user_first_name.setAttribute("name", "users_first_name");
                input_user_first_name.setAttribute("value", response_dict.first_name);
                createform.appendChild(input_user_first_name);

                var input_user_city = document.createElement('input');
                input_user_city.setAttribute("type", "text");
                input_user_city.setAttribute("name", "users_city");
                input_user_city.setAttribute("value", response_dict.city);
                createform.appendChild(input_user_city);

                var input_user_country = document.createElement('input');
                input_user_country.setAttribute("type", "text");
                input_user_country.setAttribute("name", "users_country");
                input_user_country.setAttribute("value", response_dict.country);
                createform.appendChild(input_user_country);

                var input_user_zipcode = document.createElement('input');
                input_user_zipcode.setAttribute("type", "text");
                input_user_zipcode.setAttribute("name", "users_zipcode");
                input_user_zipcode.setAttribute("value", response_dict.zipcode);
                createform.appendChild(input_user_zipcode);

                var input_user_address = document.createElement('input');
                input_user_address.setAttribute("type", "text");
                input_user_address.setAttribute("name", "users_address");
                input_user_address.setAttribute("value", response_dict.street_address);
                createform.appendChild(input_user_address);

                document.getElementById("form_id").submit();
            } else {
                show_alert('error',
                    '',
                    '<p class="text-center">The server could not be reached at this moment. <br />Please try after some time. </p>'
                );
            }
        },
        error: function(resonse){
            show_alert('error',
                '',
                '<p class="text-center">The server could not be reached at this moment. <br />Please try after some time. </p>'
            );
        }
    });
} 