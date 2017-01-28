angular.module('BookRoomApp')
.controller('LoginCtrl', function($scope, $http){

    $scope.getLogin = function() {
        return $.nano(urls['home']);
    };

    $scope.some = function () {
        $http.post($.nano(urls['some']));
    };
});