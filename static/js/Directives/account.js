app.directive('account', function(){
  return {
    scope: {
      accountInfo: '=info'
    },
    templateUrl: '../static/js/Directives/account.html'
  };
});