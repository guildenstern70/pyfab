// This is called with the results from from FB.getLoginStatus().
function statusChangeCallback(response) {
	
	console.log('>> statusChangeCallback');
	
	console.log(response);
	// The response object is returned with a status field that lets the
	// app know the current login status of the person.
	// Full docs on the response object can be found in the documentation
	// for FB.getLoginStatus().
	if (response.status === 'connected') {
		// Logged into your app and Facebook.
		loggedInToFb();
	} else if (response.status === 'not_authorized') {
		// The person is logged into Facebook, but not your app.
		$('#status').html('Please log into this app (Not Authorized)');
	} else {
		// The person is not logged into Facebook, so we're not sure if
		// they are logged into this app or not.
		$('#status').html('Please log in.');
	}
}

// This function is called when someone finishes with the Login
// Button. See the onlogin handler attached to it in the sample
// code below.
function checkLoginState() {
	
	console.log('>> checkLoginState');
	
	FB.getLoginStatus(function(response) {
		statusChangeCallback(response);
	});
}

//Here we run a very simple test of the Graph API after login is
//successful. See statusChangeCallback() for when this call is made.
function loggedInToFb() {
	
	console.log('>> loggedInToFb');
	
	console.log('Welcome!  Fetching your information.... ');
	FB.api('/me', function(response) {
		console.log('Successful login for: ' + response.name);
		console.log(JSON.stringify(response));
		$('#status').html('Thanks for logging in, ' + response.name + '!');
		
		if ($('#is_logged_into_app').val() == 'False') {
			// User is logged into FB but not into app
			console.log('>> User logged into FB but not into APP');
		} else {
			console.log('>> User logged into FB and into APP');
		}
		
		submitLogin(response.name, response.email)
		
		
	});
}

///
/// Login with FaceBook
///
function fb_login(){
    FB.login(function(response) {

        if (response.authResponse) {
            console.log('Welcome!  Fetching your information.... ');
            //console.log(response); // dump complete info
            access_token = response.authResponse.accessToken; //get access token
            user_id = response.authResponse.userID; //get FB UID
            loggedInToFb();
        } else {
            //user hit cancel button
            console.log('User cancelled login or did not fully authorize.');

        }
    }, {
        scope: 'email,public_profile'
    });
}
(function() {
    var e = document.createElement('script');
    e.src = document.location.protocol + '//connect.facebook.net/en_US/all.js';
    e.async = true;
    document.getElementById('fb-root').appendChild(e);
}());

window.fbAsyncInit = function() {
	
	console.log('>> fbAsyncInit');

	FB.init({
		appId : '1597300683824253', // FableMe.com: '732656233489141',
		xfbml : true,
		version : 'v2.2'
	});

	FB.getLoginStatus(function(response) {
		statusChangeCallback(response);
	});

};


(function(d, s, id) {
	
	console.log('>> d,s,id');
	
	var js, fjs = d.getElementsByTagName(s)[0];
	if (d.getElementById(id)) {
		return;
	}
	js = d.createElement(s);
	js.id = id;
	js.src = "//connect.facebook.net/en_US/sdk.js";
	fjs.parentNode.insertBefore(js, fjs);
}(document, 'script', 'facebook-jssdk'));

function submitLogin(name, email, nick) {
	
	console.log('>> submit login');
	
	console.log('Submitting login for '+email);
	$('#name').val(name);
	$('#email').val(email);
	$('#loginsource').val('fb0');
	$('#loginform').submit();
}

function logoutFromFb() {
	
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

