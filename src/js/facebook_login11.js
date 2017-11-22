function submitLogin(name, email, nick) {

	console.log('>> submit login');

	console.log('Submitting login for '+email);
	$('#name').val(name);
	$('#email').val(email);
	$('#loginsource').val('fb0');
	$('#loginform').submit();
}

function loggedInToFb() {

	console.log('>> loggedInToFb');

	console.log('Welcome!  Fetching your information.... ');
	FB.api('/me', function(response) {
		console.log('Successful login for: ' + response.name);
		console.log(JSON.stringify(response));
		console.log('Thanks for logging in, ' + response.name + ' (' + response.email + ')');

		if ($('#is_logged_into_app').val() == 'False') {
			// User is logged into FB but not into app
			console.log('>> User logged into FB but not into APP');
		} else {
			console.log('>> User logged into FB and into APP');
		}

		submitLogin(response.name, response.email)


	});
}

function fblogin(){
    FB.login(function(response) {

        console.log('>> fblogin');

        if (response.authResponse) {
            console.log('FB recognizes user');
            loggedInToFb();
        } else {
            //user hit cancel button
            console.log('User cancelled login or did not fully authorize.');

        }
    }, {
        scope: 'email,public_profile'
    });
}

function statusChangeCallback(response) {

	console.log('>> statusChangeCallback');

	console.log(response);
	// The response object is returned with a status field that lets the
	// app know the current login status of the person.
	// Full docs on the response object can be found in the documentation
	// for FB.getLoginStatus().
	if (response.status === 'connected') {
		// Logged into your app and Facebook.
        console.log('OK - Logged In Facebook And Authorized by FableMe');
		loggedInToFb();
	} else if (response.status === 'not_authorized') {
		// The person is logged into Facebook, but not your app.
		console.log('Logged In Facebook but Not Authorized by FableMe');
	} else {
		// The person is not logged into Facebook, so we're not sure if
		// they are logged into this app or not.
		console.log('Not logged in Facebook');
	}
}

function checkLoginState() {

	console.log('>> checkLoginState');

	FB.getLoginStatus(function(response) {
		statusChangeCallback(response);
	});

}

function logoutFromEverything() {

	console.log('>> logoutFromFb');
	try
	{
		FB.getLoginStatus(function(response) {
			console.log('>> Logging out FB status is ' + response.status);
			if (response.status != 'connected') {
				console.log('Not connected to FB: logging out');
				window.location.href = "/logout";
			}
		});

		FB.logout(function(response) {
			if (response)
				console.log(response);
			// user is now logged out
			console.log('>> user is logged out');
			window.location.href = "/logout";
		});
	}
	catch(err)
	{
		console.log('HANDLED ERR>> '+ err);
		window.location.href = "/logout";
	}

}


window.fbAsyncInit = function() {
FB.init({
  appId      : '1597300683824253',
  cookie     : true,
  xfbml      : true,
  version    : 'v2.11'
});

FB.AppEvents.logPageView();

};

(function(d, s, id){
 var js, fjs = d.getElementsByTagName(s)[0];
 if (d.getElementById(id)) {return;}
 js = d.createElement(s); js.id = id;
 js.src = "https://connect.facebook.net/en_US/sdk.js";
 fjs.parentNode.insertBefore(js, fjs);
}(document, 'script', 'facebook-jssdk'));
