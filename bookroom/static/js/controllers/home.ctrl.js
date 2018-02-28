angular.module('BookRoomApp')
.controller('HomeCtrl', function($scope, $http){
    var $this = this;

    $this.mainBook = {
        rating: '5'
    };

    $this.init = function () {
        $http.post("/", {}).then(function (ret) {
            $this.mainBook = ret.data.book;
            $this.mainReviews = ret.data.reviews;

            console.log($this.mainReviews)
        })
    };

    $this.init()
});