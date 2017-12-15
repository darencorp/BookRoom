angular.module('BookRoomApp')
.controller('SearchCtrl', function($scope, $rootScope, $http){
    var $this = this;

    $this.init = function () {
        $http.get('/search?q=${$rootScope.searchCriteria}' , {params: {'q': $this.searchCriteria}}).then(function (ret) {
            console.log(ret);
        })
    };

    $this.init();

    $rootScope.$on('search', function () {
        $this.search = $rootScope.searchCriteria;
    });
});