angular.module('BookRoomApp')
.controller('UserPageCtrl', function($scope, $rootScope){
    var $this = this;

    $this.init = function() {
       $http.post('/user', {})
    };

    $this.init()
});