app.directive('settings', function(){
  return {
    scope: {
      accountInfo: '=info'
    },
    templateUrl: '../js/Directives/settings.html'
  };
});