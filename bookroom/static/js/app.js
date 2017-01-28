var app = angular.module('BookRoomApp', [
   'ui.router'
])

.controller('AppCtrl', function($scope) {

   $scope.openLoginForm = function() {
      $.UIkit.modal('#login-form').show();
   }
});