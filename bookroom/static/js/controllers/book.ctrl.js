angular.module('BookRoomApp')
    .controller('BookCtrl', function ($scope, $http) {
        var $this = this;

        $this.newReview = '';
        $this.newBook = {
            'genre': 'Action'
        };

        $this.init = function () {
            $http.post('/book', {});

            UIkit.upload('.js-upload', {

                // url: $this.newBook.image,
                multiple: false,

                completeAll: function () {
                    UIkit.notification("Attached", {status: 'primary'});
                }

            });
        };

        $this.init();

        $this.confirmNewBook = function () {

            if ($this.newBook.name == null) {
                UIkit.notification("Name is empty", {status: 'danger'});

            } else {

                fd = new FormData();
                fd.append('image', $this.image);
                fd.append('name', $this.newBook.name);

                $http.post('/image_upload', fd, {
                    transformRequest: angular.identity,
                    headers: {'Content-Type': undefined}
                }).then(function (retu) {
                    $this.newBook.image = retu.data;
                    $http.post('/add_book', $this.newBook).then(function (ret) {
                        console.log(ret);
                    });
                });
            }
        }
    });