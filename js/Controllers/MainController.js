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