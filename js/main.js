var app = angular.module('MidiaApp', []);

$(function(){
    $('#login').popover({       
        placement: 'bottom',
        html:true,
        content:  $('#loginForm').html()
    }).on('click', function(){
      $('.btn-primary').click(function(){
       
        $.post('/',  {
            username: $('#username').val(),
            password: $('#password').val(),
        }, function(r) {
          
        })
      })
  })
})
