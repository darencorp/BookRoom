angular.module('BookRoomApp')
.controller('HomeCtrl', function($scope, $rootScope, home_service){
    var $this = this;

    $this.openUserSetting = function ()  {
        $.UIkit.modal('#user-form').show();
    };

    $rootScope.$on('updateLibrary', function (event, data) {
        $this.library = data;
    });
});