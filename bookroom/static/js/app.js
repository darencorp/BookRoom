var app = angular.module('BookRoomApp', [
    'ui.router',
    'swxSessionStorage'
])
    .config(['$httpProvider', function ($httpProvider) {
        $httpProvider.defaults.headers.common['X-Requested-With'] = 'XMLHttpRequest';
    }])

    .controller('AppCtrl', function ($scope, $rootScope, $sessionStorage) {
        $scope.init = function () {
            $scope.searchCriteria = $rootScope.searchCriteria;
        };

        $scope.openLoginForm = function () {
            UIkit.modal('#login-form').show();
        };

        $scope.searchChange = function () {
            $sessionStorage.put('searchCriteria', $rootScope.searchCriteria)
        };

        $scope.init();
    });