var app = angular.module('BookRoomApp', [
    'ui.router'
])

    .config(['$httpProvider', function ($httpProvider) {
        $httpProvider.defaults.headers.common['X-Requested-With'] = 'XMLHttpRequest';
        $httpProvider.defaults.headers.post["Content-Type"] = "application/x-www-form-urlencoded";
    }])

    .controller('AppCtrl', function ($scope) {

        $scope.openLoginForm = function () {
            $.UIkit.modal('#login-form').show();
        }
    });