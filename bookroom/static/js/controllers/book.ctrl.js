angular.module('BookRoomApp')
    .controller('BookCtrl', function ($scope, $http) {
        var $this = this;

        $this.book = {}

        $this.init = function (id) {
            $http.post('/book/' + id, {}).then(function (ret) {
                $this.book = ret.data.book;
            });
        };
    });