angular.module('BookRoomApp')
    .filter('books', function () {
        return function (items) {
            return _.filter(items, function (r) {
                return r.type == 'book'
            })
        }
    })
    .filter('users', function () {
        return function (items) {
            return _.filter(items, function (r) {
                return r.type == 'user'
            })
        }
    })
    .controller('SearchCtrl', function ($scope, $rootScope, $http) {
        var $this = this;

        $this.init = function () {
            $http.get('/search', {}).then(function (ret) {
                $rootScope.searchCriteria = ret.data.query;
                $this.query = ret.data.query;
                $this.results = ret.data.results;
                $this.genreResults = ret.data.genre_results;
            })
        };

        $this.init();

        $this.containsBooks = function () {
            return _.some($this.results, function (r) {
                return r.type == 'book'
            })
        }

        $this.containsUsers = function () {
            return _.some($this.results, function (r) {
                return r.type == 'user'
            })
        }
    });