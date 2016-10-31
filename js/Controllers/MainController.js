app.controller('MainController', ['$scope', function($scope) {

	$scope.posts = [
		{
		img: '../img/joePic.jpg',
		mainText: 'Joe Coy',
		subText: '9 Likes and 4 Comments',
		postText: 'Hey everyone, this is just an example of a post that we might put on Midia.  Most social media sights have some similarities between their posts at a base level, but there are some subtle and important differences too!',
		timeStamp: '6h',
		src: 'post'
		},
		{
		img: '../img/grandmaPic.jpg',
		mainText: 'Rose Anne Coy',
		subText: 'Playing Minecraft',
		postText:'3,000 Viewers',
		timeStamp:'10h',
		src: 'twitch'
		},
		{
		img: '../img/joePic.jpg',
		mainText: 'joeschmoe commit',
		subText: '3 commits, 47+, 10-',
		postText:'fixed CS490 project',
		timeStamp:'2h',
		src: 'github'
		},
		{
		img: '../img/michaelPic.jpg',
		mainText: 'Michael Crabill\'s facebook picture',
		subText: 'u/AmericanEagle r/funny',
		postText:'Up: 30, Down: 40, 100 comments',
		timeStamp:'1d',
		src: 'reddit'
		},
		{
		img: '../img/timPic.jpg',
		mainText: 'Tim Vincent',
		subText: '17 Likes and 5 Comments',
		postText:'Just saw some amazing cute little puppers. They\'re gonna be doggos soon I bet.',
		timeStamp:'7h'
		},
		{
		img: '../img/coreyPic.jpg',
		mainText: 'Corey Pitzo',
		subText: '0 Likes and 1 Comments' ,
		postText:'You know I think Taco Bell might be the greatest invention of all time.',
		timeStamp:'4d'
		},
		{
		img: '../img/pascalPic.jpg',
		mainText: 'Pascal Lee',
		subText: '23 Likes and 0 Comments',
		postText:'Selling my Purdue football tickets, anyone want them?',
		timeStamp:'1w'
		},
		{
		img: '../img/pascalPic.jpg',
		mainText: 'Pascal Lee',
		subText: '3 Likes and 0 Comments',
		postText:'Still have the tickets',
		timeStamp:'3d'
		},
		{
		img: '../img/pascalPic.jpg',
		mainText: 'Pascal Lee',
		subText: '1 Likes and 0 Comments',
		postText:'Please someone just take them',
		timeStamp:'1d'
		}

	];

	$scope.settingsData = {
		
	};

	$scope.accountOne = {
		name: 'bob'
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
	

}]);

