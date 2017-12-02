angular.module('BookRoomApp')
    .controller('LoginCtrl', function ($scope, $http, $window) {
        var $this = this;

        $this.user = {};

        $this.passwordEquals = true;
        $this.emailValid = true;

        $this.login = function () {
            $http({
                method: 'POST',
                url: $.nano(urls['login']),
                data: $this.user
            }).then(
                function (ret) {
                    if (ret.data.error) {
                        $.UIkit.notify(ret.data.error, {status: 'danger'})
                    } else {
                        $window.location.reload();
                    }
                }
            );
        };

        $this.openRegisterForm = function () {
            $.UIkit.modal('#register-form').show();
        };

        $this.register = function (user) {
            $http({
                method: 'POST',
                url: $.nano(urls['register']),
                data: $this.user,
                contentType: "application/json"
            }).then(
                function (ret) {
                    if (ret.data.error) {
                        $.UIkit.notify(ret.data.error.desc, {status: 'danger'});
                        switch (ret.data.error.code) {
                            case 400:
                                $this.passwordEquals = false;
                                break;
                            case 401:
                                $this.emailValid = false;
                                $this.passwordEquals = true;
                                break;
                            case 402:
                                $this.emailValid = false;
                                $this.passwordEquals = true;
                                break;
                        }
                    } else {
                        $this.passwordEquals = true;
                        $this.emailValid = true;

                        $window.location.reload();
                    }
                }
            );
        };
    });