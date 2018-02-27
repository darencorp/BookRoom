angular.module('BookRoomApp')
    .controller('CatalogueCtrl', function ($scope, $rootScope, $http) {
        var $this = this;

        $this.filter = null;

        $this.init = function () {
            $http.post('/get_catalogue', {}).then(function (ret) {
                $this.books = ret.data.books;
                $this.filter = ret.data.filter;
            })
        };

        $this.init();

        $this.openBookForm = function () {
            UIkit.modal('#new-book-form').show();
            console.log(UIkit.modal('#new-book-form'));
        }

        $this.changeFilter = function () {
            console.log($this.filter)

            $http.post('/get_catalogue', {filter: $this.filter}).then(function(ret) {
                $this.books = ret.data.books;
                $this.filter = ret.data.filter;
            });
        }

        $this.addFilter = function(genre) {
            if ($this.filter.genres.includes(genre)) {
                i = $this.filter.genres.indexOf(genre);
                $this.filter.genres.splice(i, 1);
            } else {
                $this.filter.genres.push(genre)
            }

            $this.changeFilter();
        }
    });