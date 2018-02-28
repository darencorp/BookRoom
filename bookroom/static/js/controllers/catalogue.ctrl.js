angular.module('BookRoomApp')
    .controller('CatalogueCtrl', function ($scope, $rootScope, $http) {
        var $this = this;

        $this.filter = null;

        $this.init = function () {
            $http.post('/get_catalogue', {}).then(function (ret) {
                $this.books = ret.data.books;
                $this.filter = ret.data.filter;
            })
        };

        $this.init();

        $this.openBookForm = function () {
            UIkit.modal('#new-book-form').show();
        };

        $this.changeFilter = function () {
            $http.post('/get_catalogue', {filter: $this.filter}).then(function (ret) {
                $this.books = ret.data.books;
                $this.filter = ret.data.filter;
            });
        };

        $this.deleteBook = function (name, id) {
            UIkit.modal.confirm('Are you sure that you want to delete book "' + name + '"?').then(function () {
                $http.post('/delete_book/' + id).then(function (ret) {
                    UIkit.notification({
                        message: 'Deleted!',
                        status: 'success',
                        pos: 'top-center',
                        timeout: 1000
                    });
                })
            }, function () {
            });
        }
    });