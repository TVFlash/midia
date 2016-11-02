app.directive('settings', function(){
  return {
    scope: {
      settingsInfo: '=info'
    },
    templateUrl: '../static/js/Directives/settings.html'
  };
});