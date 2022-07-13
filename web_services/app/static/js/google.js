$("#google_btn").bind('click', [], googleLogin);

var googleLogin = function() {
    gapi.load('auth2', function(){
        // Retrieve the singleton for the GoogleAuth library and set up the client.
        auth2 = gapi.auth2.init({
            client_id: GOOGLE_CLIENT_ID,
            cookiepolicy: 'single_host_origin',
            scope: 'profile email'
        });
        attachSignin(document.getElementById('google_btn'));
    });
};
function attachSignin(element) {
    auth2.attachClickHandler(element, {},
        function(googleUserData) {
            var hashValue = location.hash;  
            hashValue = hashValue.replace(/^#/, '');
            googleUser(googleUserData, hashValue);
        }, function(error) {
            // commented for now (this is for checking weather user deny the permission for google signup.)
            // alert(JSON.stringify(error, undefined, 2));
        }
    );
}
// init google function
googleLogin();

//  USED to pass Google Response to REIA
function googleUser(user, hashValue) {
    $.ajax({
        type: 'POST',
        url: '/soc_login',
        beforeSend: setHeader,
        data: {
            email : user.getBasicProfile().getEmail(),
            name : user.getBasicProfile().getName(),
            first_name : user.getBasicProfile().getGivenName(),
            last_name : user.getBasicProfile().getFamilyName(),
            profile_image : user.getBasicProfile().getImageUrl(),
            source_media : 'google',
            hash : hashValue
        },
        success: function(response) {
            // rendering function from login.js
            navigate_user(response);
        },
        error: function(response){
            alert('Unable to Process your request. \n Please try again after some time');
        }
    });
}