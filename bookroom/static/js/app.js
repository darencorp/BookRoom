var app = angular.module('BookRoomApp', [
    'ui.router'
])
    .config(['$httpProvider', function ($httpProvider) {
        $httpProvider.defaults.headers.post["Content-Type"] = "application/x-www-form-urlencoded";
        $httpProvider.defaults.headers.common['X-Requested-With'] = 'XMLHttpRequest';
    }])

    .controller('AppCtrl', function ($scope, $rootScope, $http) {

        $scope.searchCriteria = '';

        $scope.openLoginForm = function () {
            UIkit.modal('#login-form').show();
        };

        $scope.searchChange = function () {
            $rootScope.searchCriteria = $scope.searchCriteria
        };

        $scope.submitSearch = function () {
            // $scope.$emit('search', null);
            $http({
                method: 'GET',
                url: '/search',
                headers: {'Content-Type': 'application/x-www-form-urlencoded'}
            });

            $scope.searchCriteria = $rootScope.searchCriteria;
        };
    });