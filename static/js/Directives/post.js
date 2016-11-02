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
        if ($scope.postInfo.src == "post")
          return '../static/js/Directives/post.html';
        else if ($scope.postInfo.src == "twitch")
          return '../static/js/Directives/twitchPost.html';
	    else if ($scope.postInfo.src == "github")
	      return '../static/js/Directives/githubPost.html';
	    else if ($scope.postInfo.src == "reddit")
	      return '../static/js/Directives/redditPost.html';
      else if ($scope.postInfo.src == "xkcd")
        return '../static/js/Directives/xkcdPost.html';
      else if ($scope.postInfo.src == "twitter")
        return '../static/js/Directives/twitterPost.html';
      else if ($scope.postInfo.src == "hackernews")
        return '../static/js/Directives/hackernewsPost.html';
      	else 
      	  return '../static/js/Directives/post.html';
      }
    }
  };
});