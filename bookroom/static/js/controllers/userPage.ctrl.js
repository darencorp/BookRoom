angular.module('BookRoomApp')
    .controller('UserPageCtrl', function ($scope, $http, $window) {
            var $this = this;

            $this.edit = false;

            $this.user_password = {
                old_password: '',
                new_password: '',
                confirm_password: ''
            };

            $this.init = function (id) {
                UIkit.upload('.js-upload', {
                    multiple: false,

                    completeAll: function () {
                        fd = new FormData();

                        fd.append('image', $this.image);

                        $http.post('/avatar_change', fd, {
                            transformRequest: angular.identity,
                            headers: {'Content-Type': undefined}
                        }).then(function (ret) {
                            $this.user.image = ret.data.image;
                        })
                    }

                });

                $http.post('/user/' + id, {}).then(function (ret) {
                    $this.user = ret.data.user;
                    $this.book_stared = ret.data.book_stared;
                    $this.book_reviews = ret.data.book_reviews;

                });
            };

            $this.changeData = function () {
                $this.edit = true;
            };

            $this.saveChanges = function () {

                $http.post("/change_data", {
                    'fname': $this.user.first_name,
                    'lname': $this.user.last_name
                }).then(function (ret) {
                    $window.location.reload()
                });
            };

            $this.openPasswordForm = function () {
                UIkit.modal('#password-form').show()
            };

            $this.changePassword = function () {
                $http.post('/change_password', $this.user_password).then(function (ret) {
                    if (ret.data.error) {
                        UIkit.notification(ret.data.error, {status: 'danger'})
                    } else {
                        UIkit.notification('Password is changed', {status: 'success'})
                        UIkit.modal('#password-form').hide()
                    }
                })
            };
        }
    );