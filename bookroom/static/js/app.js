var app = angular.module('BookRoomApp', [
    'ui.router',
    'swxSessionStorage'
])
    .config(['$httpProvider', function ($httpProvider) {
        $httpProvider.defaults.headers.common['X-Requested-With'] = 'XMLHttpRequest';
    }])

    .directive('fileModel', [
        '$parse',
        function ($parse) {
            return {
                restrict: 'A',
                link: function (scope, element, attrs) {
                    var model = $parse(attrs.fileModel);
                    var modelSetter = model.assign;

                    element.bind('change', function () {
                        scope.$apply(function () {
                            if (attrs.multiple) {
                                modelSetter(scope, element[0].files);
                            }
                            else {
                                modelSetter(scope, element[0].files[0]);
                            }
                        });
                    });
                }
            };
        }
    ])

    .controller('AppCtrl', function ($scope, $rootScope, $sessionStorage, $http) {
        $scope.init = function () {
            if ($rootScope.searchCriteria == null)
                $scope.searchCriteria = '';
        };

        $scope.openLoginForm = function () {
            UIkit.modal('#login-form').show();
        };

        $scope.searchChange = function () {
            if ($rootScope.searchCriteria != null && $rootScope.searchCriteria.length > 0) {

                $rootScope.genreSearch = false;

                $http.post('/front_search', {'criteria': $rootScope.searchCriteria}).then(function (ret) {
                    $scope.results = ret.data;
                    UIkit.dropdown('#searchDrop').show();
                })
            }
        };

        $scope.init();

        $scope.genreSearch = function (genre) {
            $rootScope.genreSearch = true;
            return '/search?q=' + genre
        }
    });