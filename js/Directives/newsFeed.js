app.directive('newsFeed', function(){
  return {
    scope: {
      posts: '='
    },
    templateUrl: 'js/Directives/NewsFeed.html'
  };
});