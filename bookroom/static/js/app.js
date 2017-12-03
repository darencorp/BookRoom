var app = angular.module('BookRoomApp', [
    'ui.router'
])

    .config(function ($stateProvider, $urlRouterProvider) {

        $stateProvider

            .state('home', {
                url: '/',
                views: {
                    'main': {
                        templateUrl: "templates/home.html"
                    }
                }
            })

            .state('catalogue', {
                url: '/catalogue',
                views: {
                    'main': {
                        templateUrl: "templates/catalogue.html"
                    }
                }
            });

            $urlRouterProvider.otherwise('/');
    })

    .controller('AppCtrl', function ($scope) {
        $scope.openLoginForm = function () {
            UIkit.modal('#login-form').show();
        }
    });