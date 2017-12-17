angular.module('BookRoomApp')
    .controller('BookCtrl', function ($scope, $http) {
        var $this = this;

        $this.book = {};
        $this.reviews = [];

        $this.newReview = '';

        $this.init = function (id) {
            $http.post('/book/' + id, {}).then(function (ret) {
                $this.book = ret.data.book;
                $this.reviews = ret.data.reviews;

                console.log(ret.data.reviews)
            });
        };

        $this.openLoginForm = function () {
            UIkit.modal("#login-form").show();
        };

        $this.openRegisterForm = function () {
            UIkit.modal("#register-form").show();
        };

        $this.addReview = function () {

            if ($this.newReview != '') {
                var review = {
                    body: $this.newReview,
                    book: $this.book.id
                };

                $http.post('/add_review', review).then(function (ret) {
                    $http.post('/update_reviews', $this.book.id).then(function (ret) {
                        $this.reviews = ret.data.reviews;
                        $this.newReview = '';
                    })
                });
            }
        }
    });