angular.module('BookRoomApp')
    .controller('CatalogueCtrl', function ($scope, $rootScope, $http) {
        var $this = this;

        $this.filter = null;

        $this.newBook = {
            'genre': 'Action'
        };

        $this.init = function () {
            $http.post('/get_catalogue', {}).then(function (ret) {
                $this.books = ret.data.books;
                $this.filter = ret.data.filter;
            })
        };

        $this.init();

        $this.openBookForm = function (book) {
            UIkit.modal('#new-book-form').show();

            if(book == null) {
                $scope.$emit('editBook', {book: $this.newBook});
            } else {
                $scope.$emit('editBook', {book: book});
            }
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
                    if (ret.data) {
                        UIkit.notification({
                            message: 'Deleted!',
                            status: 'success',
                            pos: 'top-center',
                            timeout: 1000
                        });

                        $this.init();
                    } else {
                        UIkit.notification({
                            message: 'Error!',
                            status: 'danger',
                            pos: 'top-center',
                            timeout: 1000
                        });
                    }
                })
            }, function () {
            });
        }

        $rootScope.$on('refreshCatalogue', function (event) {
            $this.init();
        })
    });