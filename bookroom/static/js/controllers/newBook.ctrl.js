angular.module('BookRoomApp')
    .controller('NewBookCtrl', function ($scope, $rootScope, $http) {
        var $this = this;

        $this.newBook = {
            'genre': 'Action'
        };

        $this.imgPreview = '';

        $this.init = function () {
            UIkit.upload('.js-upload', {

                // url: $this.newBook.image,
                multiple: false,

                completeAll: function () {
                    var reader = new FileReader();
                    reader.onload = $this.imageIsLoaded;
                    reader.readAsDataURL($this.image);

                    $this.newBook.image = $this.image;
                }

            });
        };

        $this.init();

        $this.imageIsLoaded = function (e) {
            $scope.$apply(function () {
                $this.imgPreview = e.target.result;
            });
        };

        $this.confirmNewBook = function () {

            if ($this.newBook.name == null || $this.newBook.name == '') {
                UIkit.notification("Name is empty", {status: 'danger'});
            } else {

                fd = new FormData();

                fd.append('image', $this.newBook.image);
                fd.append('name', $this.newBook.name);
                fd.append('id', $this.newBook.id);

                $http.post('/image_upload', fd, {
                    transformRequest: angular.identity,
                    headers: {'Content-Type': undefined}
                }).then(function (retu, error) {
                    if (error) {
                        UIkit.notification("Something wrong with image", {status: 'danger'});
                    } else {
                        $this.newBook.image = retu.data;
                        $http.post('/add_book', $this.newBook).then(function (ret) {
                            if (!ret.data.id) {
                                UIkit.notification("Book is added", {status: 'success'});
                            } else {
                                UIkit.notification("Book is updated", {status: 'success'});
                            }

                            UIkit.modal('#new-book-form').hide();

                            $scope.$emit('refreshCatalogue', {});
                        });

                        $this.newBook = {
                            'genre': 'Action'
                        };

                        $this.imgPreview = '';
                    }
                });
            }
        };

        $rootScope.$on('editBook', function (event, data) {
            $this.newBook = data.book;
            if (data.book. image) {
                $this.imgPreview = '/static/img/books/' + data.book.image;
            }
        });
    });