app.controller('MainController', ['$scope', '$window', function($scope, $window) {

	$scope.posts = [
		{
		img: '../static/img/joePic.jpg',
		mainText: 'Joe Coy',
		subText: '9 Likes and 4 Comments',
		postText: 'Hey everyone, this is just an example of a post that we might put on Midia.  Most social media sights have some similarities between their posts at a base level, but there are some subtle and important differences too!',
		timeStamp: '6h',
		src: 'post'
		},
		{
		img: '../static/img/grandmaPic.jpg',
		mainText: 'Rose Anne Coy',
		subText: 'Playing Minecraft',
		postText:'3,000 Viewers',
		timeStamp:'10h',
		src: 'twitch'
		},
		{
		img: '../static/img/joePic.jpg',
		mainText: 'joeschmoe commit',
		subText: '3 commits, 47+, 10-',
		postText:'fixed CS490 project',
		timeStamp:'2h',
		src: 'github'
		},
		{
		img: '../static/img/michaelPic.jpg',
		mainText: 'Michael Crabill\'s facebook picture',
		subText: 'u/AmericanEagle r/funny',
		postText:'Up: 30, Down: 40, 100 comments',
		timeStamp:'1d',
		src: 'reddit'
		},
		{
		img: '../static/img/xkcdContent.png',
		mainText: 'Purity Ranking',
		subText: 'Permanent link to this comic: http://xkcd.com/435/',
		postText:'Image URL (for hotlinking/embedding): http://imgs.xkcd.com/comics/purity.png',
		timeStamp:'3d',
		src: 'xkcd'
		},
		{
		img: '../static/img/coreyPic.jpg',
		mainText: 'Corey Pitzo',
		subText: '@coreyLoLgod',
		postText:'TSM4lyfe',
		timeStamp:'3m',
		src: 'twitter'
		},
		{
		mainText: 'Facebook Q3 2016 Results',
		subText: '23 points by tvincent',
		timeStamp:'3h',
		src: 'hackernews'
		},
		{
		img: '../static/img/timPic.jpg',
		mainText: 'Tim Vincent',
		subText: '17 Likes and 5 Comments',
		postText:'Just saw some amazing cute little puppers. They\'re gonna be doggos soon I bet.',
		timeStamp:'7h'
		},
		{
		img: '../static/img/coreyPic.jpg',
		mainText: 'Corey Pitzo',
		subText: '0 Likes and 1 Comments' ,
		postText:'You know I think Taco Bell might be the greatest invention of all time.',
		timeStamp:'4d'
		},
		{
		img: '../static/img/pascalPic.jpg',
		mainText: 'Pascal Lee',
		subText: '23 Likes and 0 Comments',
		postText:'Selling my Purdue football tickets, anyone want them?',
		timeStamp:'1w'
		},
		{
		img: '../static/img/pascalPic.jpg',
		mainText: 'Pascal Lee',
		subText: '3 Likes and 0 Comments',
		postText:'Still have the tickets',
		timeStamp:'3d'
		},
		{
		img: '../static/img/pascalPic.jpg',
		mainText: 'Pascal Lee',
		subText: '1 Likes and 0 Comments',
		postText:'Please someone just take them',
		timeStamp:'1d'
		}

	];

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
			    	$scope.accountOne.id = response.ID;
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
    var pack = {}
    pack.token = user.accessToken
    $.ajax({
      type: "POST", 
      url: "/api/login/" + user.userID,
      data: JSON.stringify(pack),
      contentType: "application/json"
    }).done(function(data){
        console.log("[Request sent]")
    })
  }

  function getPageData(){
  	$.ajax({
      type: "POST", 
      url: "/api/refresh/" + $scope.accountOne.id,
      contentType: "application/json"
    }).done(function(data){
        console.log("[Request sent]")
        $scope.posts = $.parseJSON(data);
    })
  }
  	//getPageData();
	//setInterval(getPageData, 15*1000);



}]);

