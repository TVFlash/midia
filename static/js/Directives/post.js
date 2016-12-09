app.directive('post', function(){
  return {
    scope: {
      postInfo: '=info'
    },
    
    template: '<ng-include src="getTemplateUrl()"/>',
    controller: function($scope) {
      //function used on the ng-include to resolve the template
  $scope.getPicture = function(){
    return $scope.$parent.pictureURL;
  } 

  $scope.CallAdd = function(){
        if ($scope.postInfo.type == "facebook")
          return $scope.$parent.addfb();
        else if ($scope.postInfo.type == "twitch")
         return $scope.$parent.addtwitch();
        else if ($scope.postInfo.type == "github")
          return $scope.$parent.addgh();
        else if ($scope.postInfo.type == "reddit")
          return $scope.$parent.addreddit();
        else if ($scope.postInfo.type == "xkcd")
          return $scope.$parent.xkcd();
        else if ($scope.postInfo.type == "twitter")
          return $scope.$parent.addtweet();
        else if ($scope.postInfo.type == "hackernews")
          return $scope.$parent.addhn();
        else 
          return $scope.$parent.addfb();
      }
      $scope.getTemplateUrl = function() {
        //basic handling
        if ($scope.postInfo.type == "facebook")
          return '../static/js/Directives/post.html';
        else if ($scope.postInfo.type == "twitch")
          return '../static/js/Directives/twitchPost.html';
      else if ($scope.postInfo.type == "github")
        return '../static/js/Directives/githubPost.html';
      else if ($scope.postInfo.type == "reddit")
        return '../static/js/Directives/redditPost.html';
      else if ($scope.postInfo.type == "xkcd")
        return '../static/js/Directives/xkcdPost.html';
      else if ($scope.postInfo.type == "twitter")
        return '../static/js/Directives/twitterPost.html';
      else if ($scope.postInfo.type == "hackernews")
        return '../static/js/Directives/hackernewsPost.html';
        else 
          return '../static/js/Directives/post.html';
      }
    }
  };
});