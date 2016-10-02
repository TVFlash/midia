app.directive('post', function(){
  return {
    scope: {
      postInfo: '=info'
    },
    templateUrl: '../js/Directives/post.html'
  };
});