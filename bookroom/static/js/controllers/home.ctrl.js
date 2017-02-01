angular.module('BookRoomApp')
.controller('HomeCtrl', function($scope, $rootScope, home_service){
    var $this = this;

    $this.openBookForm = function (id)  {
        home_service.getBook(id, function (ret) {
            $rootScope.$emit('showBookForm', ret.data);
        });
    };

    $rootScope.$on('showBookForm', function (event, data) {
        $this.book = data.book;
        $.UIkit.modal('#book-form').show();
    });

    $this.saveMarketBook = function(book) {
        home_service.saveMarketBook(book);
    };

    $this.getBooks = function () {
        home_service.getBooks(function(ret) {
            $this.books = ret.data.books;
        });
    };

    $this.getBooks();
});