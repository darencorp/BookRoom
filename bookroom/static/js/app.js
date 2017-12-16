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