$("#fb_btn").bind('click', [],facebookLogin);

(function(d, s, id){
    var js, fjs = d.getElementsByTagName(s)[0];
    if (d.getElementById(id)) {return;}
    js = d.createElement(s); js.id = id;
    js.src = "https://connect.facebook.net/en_US/sdk.js";
    fjs.parentNode.insertBefore(js, fjs);
}(document, 'script', 'facebook-jssdk'));

function facebookLogin(){
    FB.login(function(response) {
        if (response.authResponse) {
            if (response.status === 'connected') {
                // for first time user it will ask permissions for login to our website.
                // checking required fields are checked are not in permission popup.
                FB.api('/me/permissions', function(response) {
                    var declined = [];
                    for (i = 0; i < response.data.length; i++) {
                        // checking unchecked fields in permission popup
                        if (response.data[i].status == 'declined') {
                            declined.push(response.data[i].permission);
                        }
                    }
                    // if email field is not checked in permission popup it will go basic login flow
                    for(i=0; i<=declined.length; i++){
                        if(declined[i] == 'email'){
                            try {
                                if($('#loginModal').data('bs.modal').isShown == true){
                                    $('#loginModal').modal('hide');
                                    $("#permissionModal").modal('show');
                                    $("#permission_btn")
                                        .removeAttr('onclick')
                                        .attr('onclick', "facebookLogin()");
                                }
                            }
                            catch(err) {
                                $("#permissionModal").modal('show');
                            }
                            return false;
                        }
                        else{
                            var hashValue = location.hash;  
                            hashValue = hashValue.replace(/^#/, '');
                            get_user_details(hashValue);
                        }
                    }
                });
            } else if (response.status === 'not_authorized') {
                alert('you are not authorized');
            } else {
                // The person is not logged into Facebook, so we're not sure if
                // they are logged into this app or not.
            }
        }else{
            alert("it's mandatory to signup using social media");
        }
    }, {
            // scope fields will show to ask permission for first time user in our website.
            scope: 'public_profile,email,user_birthday,user_likes,user_friends,user_location,user_hometown,read_custom_friendlists',
            force:true,
            auth_type:'rerequest'
        });
}


function get_user_details(hashValue){
    FB.api('/me',{fields:'first_name,last_name,email,gender,birthday,verified'},
        function(response) {
        var myBD = response.birthday;
        // Update Hidden inputs
        var birthday = "";
        if (typeof myBD != 'undefined'){
            var fb_date = response.birthday;
            var fb_date_array = fb_date.split('/');
            birthday = fb_date_array[2]+"-"+fb_date_array[0]+"-"+fb_date_array[1];
        }
        $.ajax({
            type: "POST",
            url: "/soc_login",
            beforeSend: setHeader,
            data : {
                first_name : response.first_name,
                last_name  : response.last_name,
                email  : response.email,
                birthday : birthday,
                gender : response.gender,
                source_media : 'facebook',
                hash : hashValue,
            },
            success:function(response) {
                // rendering function from login.js
                navigate_user(response);
            },
            error: function(response){
                alert('Unable to Process your request right now \n Please try again afte sometime');
            }
        });
    });
}
