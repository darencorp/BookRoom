angular.module('BookRoomApp')
.controller('BookCtrl', function($scope, $http){
    var $this = this;

    $this.newReview = '';

    $this.init = function () {
        $http.post('/book', {});
    };

    $this.init();
});