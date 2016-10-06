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

	$scope.loginFunc = function(){
    $('#login').popover({       
        placement: 'left',
        html:true,
        content:  $('#loginForm').html()
    }).on('click', function(){
    	$scope.userLoggedIn = true;
      // $('.btn-primary').click(function(){
       
      //   $.post('/',  {
      //       username: $('#username').val(),
      //       password: $('#password').val(),
      //   }, function(r) {
          
      //   })
      // })
      $('#createAccBtn').on('click', function(){
		window.open("http://www.facebook.com/signup");
	})
  })
};

}]);
