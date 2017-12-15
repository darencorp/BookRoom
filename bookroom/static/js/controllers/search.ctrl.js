angular.module('BookRoomApp')
.controller('SearchCtrl', function($scope, $rootScope, $http, $sessionStorage){
    var $this = this;

    $this.init = function () {
        $rootScope.searchCriteria = $sessionStorage.get('searchCriteria');
        $http.get('/search?q=${$sessionStorage.searchCriteria}' , {params: {'q': $this.searchCriteria}}).then(function (ret) {
            //show results
        })
    };

    $this.init();
});