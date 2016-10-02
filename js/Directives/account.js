app.directive('account', function(){
  return {
    scope: {
      name: '=',
      img: '='
    },
    templateUrl: 'js/Directives/account.html'
  };
});