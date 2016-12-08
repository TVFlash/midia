app.controller('MainController', ['$scope', '$window', function($scope, $window) {

	$scope.displayLoadingGIF = true;
	$scope.posts = [];
	/*$scope.posts = [
		{
		picture: '../static/img/joePic.jpg',
		mainText: 'Joe Coy',
		subText: '9 Likes and 4 Comments',
		message: 'Hey everyone, this is just an example of a post that we might put on Midia.  Most social media sights have some similarities between their posts at a base level, but there are some subtle and important differences too!',
		time: '6h',
		source: 'post'
		},
		{
		picture: '../static/img/grandmaPic.jpg',
		mainText: 'Rose Anne Coy',
		subText: 'Playing Minecraft',
		message:'3,000 Viewers',
		time:'10h',
		source: 'twitch'
		},
		{
		picture: '../static/img/joePic.jpg',
		mainText: 'joeschmoe commit',
		subText: '3 commits, 47+, 10-',
		message:'fixed CS490 project',
		time:'2h',
		source: 'github'
		},
		{
		picture: '../static/img/michaelPic.jpg',
		mainText: 'Michael Crabill\'s facebook picture',
		subText: 'u/AmericanEagle r/funny',
		message:'Up: 30, Down: 40, 100 comments',
		time:'1d',
		source: 'reddit'
		},
		{
		picture: '../static/img/timPic.jpg',
		mainText: 'Tim Vincent',
		subText: '17 Likes and 5 Comments',
		message:'Just saw some amazing cute little puppers. They\'re gonna be doggos soon I bet.',
		time:'7h'
		},
		{
		picture: '../static/img/coreyPic.jpg',
		mainText: 'Corey Pitzo',
		subText: '0 Likes and 1 Comments' ,
		message:'You know I think Taco Bell might be the greatest invention of all time.',
		time:'4d'
		},
		{
		picture: '../static/img/pascalPic.jpg',
		mainText: 'Pascal Lee',
		subText: '23 Likes and 0 Comments',
		message:'Selling my Purdue football tickets, anyone want them?',
		time:'1w'
		},
		{
		picture: '../static/img/pascalPic.jpg',
		mainText: 'Pascal Lee',
		subText: '3 Likes and 0 Comments',
		message:'Still have the tickets',
		time:'3d'
		},
		{
		picture: '../static/img/pascalPic.jpg',
		mainText: 'Pascal Lee',
		subText: '1 Likes and 0 Comments',
		message:'Please someone just take them',
		time:'1d'
		}

	];*/

	$scope.settingsData = {
		
	};

	$scope.accountOne = {
		name: 'user',
		id: 0
	};

	$scope.userLoggedIn = false;
	$scope.username = '';

	$scope.logoutFunc = function(){
		$scope.userLoggedIn = false;
		$('#login').popover('show');
	};


	/*$scope.loginFunc = function(){
	    	
		$('#loginBtn').click(function(){
	       	
	      //   $.post('/',  {
	      //       username: $('#username').val(),
	      //       password: $('#password').val(),
	      //   }, function(r) {
	          
	      //   })
		    $scope.$apply(function(){
		    	$scope.userLoggedIn = true;
		    	$scope.username = 'bob';
		    	$('#login').popover('hide');
		    });
	    })

	    
	    
	    $('#createAccBtn').on('click', function(){
			window.open("http://www.facebook.com/signup");
		})

	    $('#forgotPassword').on('click', function(){
			window.open("http://www.facebook.com/signup");
		})


	};*/


	/*var initPopover = function(){
	    $('#login').popover({       
	        placement: 'left',
	        html:true,
	        content:  $('#loginForm').html()
	    }).on('click', $scope.loginFunc())
	};
	initPopover();*/

	$scope.loginFunc = function(){
		FB.login(function(response){
	    statusChangeCallback(response);
	  },{scope:"user_status user_posts"});
	};

	$scope.saveFunc = function() {
		// check all textboxes
		if ($('#priorityfb').val().length > 0) {
			var pack = {
				priority: $('#priorityfb').val()
			}
			$.ajax({
		      type: "POST", 
		      url: "/api/update/" + $scope.accountOne.id + "/facebook/" + $scope.accountOne.name,
		      data: JSON.stringify(pack),
		      contentType: "application/json"
		    }).done(function(data){
		        console.log("[Request sent]");
		    })
			// make request here
		}
		if ($('#usernametweet').val().length > 0) {
			var pack = {
				username: $('#usernametweet').val()
			}
			$.ajax({
		      type: "POST", 
		      url: "/api/update/" + $scope.accountOne.id + "/twitter/" + $('#usernametweet').val(),
		      data: JSON.stringify(pack),
		      contentType: "application/json"
		    }).done(function(data){
		        console.log("[Request sent]");
		    })
			// make request here

		}
		if ($('#usernametwitch').val().length > 0) {
			var pack = {
				username: $('#usernametwitch').val()
			}
			$.ajax({
		      type: "POST", 
		      url: "/api/update/" + $scope.accountOne.id + "/twitch/" + $('#usernametwitch').val(),
		      data: JSON.stringify(pack),
		      contentType: "application/json"
		    }).done(function(data){
		        console.log("[Request sent]");
		    })
			// make request here
		}
		if ($('#usernamegh').val().length > 0) {
			var pack = {
				username: $('#usernamegh').val()
			}
			$.ajax({
		      type: "POST", 
		      url: "/api/update/" + $scope.accountOne.id + "/github/" + $('#usernamegh').val(),
		      data: JSON.stringify(pack),
		      contentType: "application/json"
		    }).done(function(data){
		        console.log("[Request sent]");
		    })
			// make request here
		}
		if ($('#usernamehn').val().length > 0) {
			var pack = {
				username: $('#usernamehn').val()
			}
			$.ajax({
		      type: "POST", 
		      url: "/api/update/" + $scope.accountOne.id + "/hackernews/" + $('#usernamehn').val(),
		      data: JSON.stringify(pack),
		      contentType: "application/json"
		    }).done(function(data){
		        console.log("[Request sent]");
		    })
			// make request here
		}
		if ($('#usernamexkcd').val().length > 0) {
			var pack = {
				username: $('#usernamexkcd').val()
			}
			$.ajax({
		      type: "POST", 
		      url: "/api/update/" + $scope.accountOne.id + "/xkcd/" + $('#usernamexkcd').val(),
		      data: JSON.stringify(pack),
		      contentType: "application/json"
		    }).done(function(data){
		        console.log("[Request sent]");
		    })
			// make request here
		}
		if ($('#usernamereddit').val().length > 0) {
			// make request here
			var pack = {
				username: $('#usernamereddit').val()
			}
			$.ajax({
		      type: "POST", 
		      url: "/api/update/" + $scope.accountOne.id + "/reddit/" + $('#usernamereddit').val(),
		      data: JSON.stringify(pack),
		      contentType: "application/json"
		    }).done(function(data){
		        console.log("[Request sent]");
		    })
		}
	};

	$scope.addfb = function() {
		var pack = {}
		$.ajax({
		      type: "POST", 
		      url: "/api/interaction/" + $scope.accountOne.id + "/facebook/" + $scope.accountOne.name,
		      data: JSON.stringify(pack),
		      contentType: "application/json"
		    }).done(function(data){
		        console.log("[Request sent]");
		    })
	}

	$scope.addtweet = function() {
		var pack = {}
		$.ajax({
		      type: "POST", 
		      url: "/api/interaction/" + $scope.accountOne.id + "/twitter/" + $('#usernametweet').val(),
		      data: JSON.stringify(pack),
		      contentType: "application/json"
		    }).done(function(data){
		        console.log("[Request sent]");
		    })
	}

	$scope.addtwitch = function() {
		var pack = {}
		$.ajax({
		      type: "POST", 
		      url: "/api/interaction/" + $scope.accountOne.id + "/twitch/" + $('#usernametwitch').val(),
		      data: JSON.stringify(pack),
		      contentType: "application/json"
		    }).done(function(data){
		        console.log("[Request sent]");
		    })
	}

	$scope.addgh = function() {
		var pack = {}
		$.ajax({
		      type: "POST", 
		      url: "/api/interaction/" + $scope.accountOne.id + "/github/" + $('#usernamegh').val(),
		      data: JSON.stringify(pack),
		      contentType: "application/json"
		    }).done(function(data){
		        console.log("[Request sent]");
		    })
	}

	$scope.addhn = function() {
		console.log("/api/interaction/" + $scope.accountOne.id + "/hackernews/" + $('#usernamehn').val());
		var pack = {}
		$.ajax({
		      type: "POST", 
		      url: "/api/interaction/" + $scope.accountOne.id + "/hackernews/" + $('#usernamehn').val(),
		      data: JSON.stringify(pack),
		      contentType: "application/json"
		    }).done(function(data){
		        console.log("[Request sent]");
		    })
	}

	$scope.addxkcd = function() {
		var pack = {}
		$.ajax({
		      type: "POST", 
		      url: "/api/interaction/" + $scope.accountOne.id + "/xkcd/" + $('#usernamexkcd').val(),
		      data: JSON.stringify(pack),
		      contentType: "application/json"
		    }).done(function(data){
		        console.log("[Request sent]");
		    })
	}

	$scope.addreddit = function() {
		var pack = {}
		$.ajax({
		      type: "POST", 
		      url: "/api/interaction/" + $scope.accountOne.id + "/reddit/" + $('#usernamereddit').val(),
		      data: JSON.stringify(pack),
		      contentType: "application/json"
		    }).done(function(data){
		        console.log("[Request sent]");
		    })
	}

  // This is called with the results from from FB.getLoginStatus().
  function statusChangeCallback(response) {
    console.log('statusChangeCallback');
    // The response object is returned with a status field that lets the
    // app know the current login status of the person.
    // Full docs on the response object can be found in the documentation
    // for FB.getLoginStatus().
    if (response.status === 'connected') {
      // Logged into your app and Facebook.
      testAPI();
      console.log(response.authResponse)
      loadUserData(response.authResponse);
      FB.api('/me', function(response) {
       			$scope.$apply(function(){
			    	$scope.userLoggedIn = true;
			    	$scope.accountOne.name = response.name;
			    	
			    });
     		});

    } else if (response.status === 'not_authorized') {
      // The person is logged into Facebook, but not your app.
      document.getElementById('status').innerHTML = 'Please log ' +
        'into this app.';
    } else {
      // The person is not logged into Facebook, so we're not sure if
      // they are logged into this app or not.
      document.getElementById('status').innerHTML = 'Please log ' +
        'into Facebook.';
    }
  }

  // This function is called when someone finishes with the Login
  // Button.  See the onlogin handler attached to it in the sample
  // code below.
  function checkLoginState() {
    FB.getLoginStatus(function(response) {
      statusChangeCallback(response);
    });
  }

  window.fbAsyncInit = function() {
  FB.init({
    appId      : '524150327779866',
    cookie     : true,  // enable cookies to allow the server to access 
                        // the session
    xfbml      : true,  // parse social plugins on this page
    version    : 'v2.3', // use graph api version 2.7
  });

  

  // Now that we've initialized the JavaScript SDK, we call 
  // FB.getLoginStatus().  This function gets the state of the
  // person visiting this page and can return one of three states to
  // the callback you provide.  They can be:
  //
  // 1. Logged into your app ('connected')
  // 2. Logged into Facebook, but not your app ('not_authorized')
  // 3. Not logged into Facebook and can't tell if they are logged into
  //    your app or not.
  //
  // These three cases are handled in the callback function.

  FB.getLoginStatus(function(response) {
    statusChangeCallback(response);
  });

  };

  // Load the SDK asynchronously
  (function(d, s, id) {
    var js, fjs = d.getElementsByTagName(s)[0];
    if (d.getElementById(id)) return;
    js = d.createElement(s); js.id = id;
    js.src="https://connect.facebook.net/en_US/all.js";
    fjs.parentNode.insertBefore(js, fjs);
  }(document, 'script', 'facebook-jssdk'));

  // Here we run a very simple test of the Graph API after login is
  // successful.  See statusChangeCallback() for when this call is made.
  function testAPI() {
    console.log('Welcome!  Fetching your information.... ');
    FB.api('/me', function(response) {
      console.log('Successful login for: ' + response.name);
      document.getElementById('status').innerHTML =
        'Thanks for logging in, ' + response.name + '!';
    });
  }

  function loadUserData(user) {
    console.log("User : " + user.userID);
    $scope.accountOne.id = user.userID;
    var pack = {}
    pack.token = user.accessToken
    $.ajax({
      type: "POST", 
      url: "/api/login/" + user.userID,
      data: JSON.stringify(pack),
      contentType: "application/json"
    }).done(function(data){
        console.log("[Request sent]")
	getPageData();
    })
  }

  function getPageData(){
    $.ajax({
      type: "POST", 
      url: "/api/refresh/" + $scope.accountOne.id,
      contentType: "application/json"
    }).done(function(data){
        console.log("[Request sent for refresh]");
        $scope.posts = $scope.posts.concat($.parseJSON(data));
        console.log($scope.posts);
        $scope.displayLoadingGIF = false;
        $scope.$apply();
    })
  }

	setInterval(getPageData, 15*1000);




}]);

