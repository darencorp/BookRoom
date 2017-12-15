angular.module('BookRoomApp')
.controller('HomeCtrl', function($scope, $http){
    var $this = this;

    $this.openUserSetting = function ()  {
        UIkit.modal("#login-form").show();
    };
});