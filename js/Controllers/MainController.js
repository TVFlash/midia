app.controller('MainController', ['$scope', function($scope) {

	$scope.posts = [
		{
		img: '../img/test.png',
		text: 'facebook text'
		},
		{
		img: '../img/test.png',
		text: 'facebook2 text'
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