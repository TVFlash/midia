app.controller('MainController', ['$scope', function($scope) {

	$scope.posts = [
		{
		img: '../img/test.png',
		text: 'Joe Coy',
		subText: '9 Likes and 4 Comments'
		},
		{
		img: '../img/test.png',
		text: 'facebook2 text',
		subText: '9 Likes and 4 Comments'
		}
	];

	$scope.accountOne = {
		name: 'bob'
	};

}]);

$(function(){
    $('#login').popover({       
        placement: 'left',
        html:true,
        content:  $('#loginForm').html()
    }).on('click', function(){
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
})