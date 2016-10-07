app.controller('MainController', ['$scope', function($scope) {

	$scope.posts = [
		{
		img: '../img/test.png',
		mainText: 'Joe Coy',
		subText: '9 Likes and 4 Comments',
		postText: 'Hey everyone, this is just an example of a post that we might put on Midia.  Most social media sights have some similarities between their posts at a base level, but there are some subtle and important differences too!',
		timeStamp: '6h'
		},
		{
		img: '../img/test.png',
		mainText: 'facebook2 text',
		subText: 'subText',
		postText:'postText',
		timeStamp:'time'
		}
	];

	$scope.accountOne = {
		name: 'bob'
	};

	$scope.userLoggedIn = false;
	$scope.username = '';

	$scope.logoutFunc = function(){
		$scope.userLoggedIn = false;
		$('#login').popover('show');
	};

	$scope.loginFunc = function(){
	    	
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
	};


	var initPopover = function(){
	    $('#login').popover({       
	        placement: 'left',
	        html:true,
	        content:  $('#loginForm').html()
	    }).on('click', $scope.loginFunc())
	};
	initPopover();
	

}]);

