var linkedin_btn = $("#linkedin_btn");
linkedin_btn.bind('click', [], onLinkedInLoad);

function onLinkedInLoad() {
    IN.UI.Authorize().place();
    IN.Event.on(IN, "auth", onLinkedInAuth);
}

function onLinkedInAuth(){
    IN.API.Profile("me")
        .fields(
            "firstName", 
            "lastName", 
            "industry", 
            "location:(name)", 
            "picture-url", 
            "headline", 
            "summary", 
            "num-connections", 
            "public-profile-url", 
            "distance", 
            "positions", 
            "email-address", 
            "educations",
            "date-of-birth"
        )
        .result(getProfileData)
        .error(getProfileError);
}

function getProfileData(profile_data){
    var member = profile_data.values[0];
    var hashValue = location.hash;
    hashValue = hashValue.replace(/^#/, '');
    $.ajax({
        type: "POST",
        url : "/soc_login",
        beforeSend: setHeader,
        data: {
            first_name: member.firstName,
            last_name : member.lastName,
            email     : member.emailAddress,
            gender    : 'Male',
            birthday  : '1990-07-11',
            source_media : 'linkedin',
            hash: hashValue,
        },
        success:function(response) {
            // rendering function from login.js
            navigate_user(response);
        },
        error: function(response){
            alert('Unable to Process your request. \n Please try again after some time');
        }
    });
}

function getProfileError(error){
    alert('Unable to Signup/Login with Linkedin right now \n Please try again later or use some other social media to Login/Signup');
}