app.directive('post', function(){
  return {
    scope: {
      postInfo: '=info'
    },

    /*templateUrl: function(elem, attr) {
    	if(attr.template === undefined)
    		return '../js/Directives/post.html';
    	else
      		return '../js/Directives/'+attr.template+'.html'; 
    }*/
    template: '<ng-include src="getTemplateUrl()"/>',
    controller: function($scope) {
      //function used on the ng-include to resolve the template
      $scope.getTemplateUrl = function() {
        //basic handling
        if ($scope.postInfo.src == "post")
          return '../js/Directives/post.html';
        else if ($scope.postInfo.src == "twitch")
          return '../js/Directives/twitchPost.html';
	    else if ($scope.postInfo.src == "github")
	      return '../js/Directives/githubPost.html';
	    else if ($scope.postInfo.src == "reddit")
	      return '../js/Directives/redditPost.html';
      	else 
      	  return '../js/Directives/post.html';
      }
    }
  };
});