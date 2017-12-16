angular.module('BookRoomApp')
    .controller('CatalogueCtrl', function ($scope, $rootScope, $http) {
        var $this = this;

        $this.init = function () {
            $http.get('/catalogue', {}).then(function (ret) {
                $this.books = ret.data.books;
            })
        };

        $this.init();

        $this.openBookForm = function () {
            UIkit.modal('#new-book-form').show();
            console.log(UIkit.modal('#new-book-form'));
        }
    });