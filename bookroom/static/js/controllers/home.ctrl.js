angular.module('BookRoomApp')
.controller('HomeCtrl', function($scope){
    $scope.getExitUrl = function () {
        return $.nano(urls['index']);
    };
});