angular.module('BookRoomApp')
    .filter('reverse', function () {
        return function (items) {
            return items.slice().reverse();
        }
    })
    .controller('BookCtrl', function ($scope, $rootScope, $http) {
        var $this = this;

        $this.book = {};
        $this.reviews = [];

        $this.rating = '0';
        $this.my_rating = '';

        $this.newReview = '';

        $this.init = function (id) {
            $http.post('/book/' + id, {}).then(function (ret) {
                $this.book = ret.data.book;
                $this.reviews = ret.data.reviews;
                $this.rating = ret.data.avg_rating + '';
                $this.my_rating = ret.data.user_rating || '';
            });
        };

        $this.print = function () {
            console.log($this.rating);
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
        };

        $this.voteBook = function () {

            var vote = {
                book_id: $this.book.id,
                rating: $this.rating
            };

            $http.post('/vote_book', vote).then(function (ret) {
                $this.my_rating = $this.rating;
                $this.rating = ret.data.avg_rating + '';
            });
        };

        $this.voteReview = function (review_id, rating) {

            var vote = {
                review_id: review_id,
                rating: rating
            };

            $http.post('/vote_review', vote).then(function (ret) {

                var r = _.find($this.reviews, function(review){ return review.id == review_id; });

                r.true_rating = ret.data.review.true_rating;
                r.false_rating = ret.data.review.false_rating;
                r.user_vote = rating;
            });
        }
    });