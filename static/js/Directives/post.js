app.directive('post', function(){
  return {
    scope: {
      postInfo: '=info'
    },
    
    template: '<ng-include src="getTemplateUrl()"/>',
    controller: function($scope) {
      //function used on the ng-include to resolve the template
      $scope.getTemplateUrl = function() {
        //basic handling
        if ($scope.postInfo.source == "post")
          return '../static/js/Directives/post.html';
        else if ($scope.postInfo.source == "twitch")
          return '../static/js/Directives/twitchPost.html';
	    else if ($scope.postInfo.source == "github")
	      return '../static/js/Directives/githubPost.html';
	    else if ($scope.postInfo.source == "reddit")
	      return '../static/js/Directives/redditPost.html';
      	else 
      	  return '../static/js/Directives/post.html';
      }
    }
  };
});