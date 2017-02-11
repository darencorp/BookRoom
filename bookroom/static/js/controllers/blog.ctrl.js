angular.module('BookRoomApp')
.controller('BlogCtrl', function($scope, $http){

    $scope.post = {};

    $scope.addPost = function (post) {
        $http({method: 'POST', url: $.nano(urls['post_add']), data: post }).then(
            function (ret) {

            });
    }

});