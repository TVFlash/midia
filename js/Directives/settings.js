app.directive('settings', function(){
  return {
    scope: {
      settingsInfo: '=info'
    },
    templateUrl: '../js/Directives/settings.html'
  };
});