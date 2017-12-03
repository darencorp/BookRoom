angular.module('BookRoomApp')
.controller('HomeCtrl', function($scope, $rootScope){
    var $this = this;

    $this.openUserSetting = function ()  {
        UIkit.modal("#login-form").show();
    };

    $rootScope.$on('updateLibrary', function (event, data) {
        $this.library = data;
    });
});