app.directive('account', function(){
  return {
    scope: {
      accountInfo: '@info'
    },
    templateUrl: '../js/Directives/account.html'
  };
});