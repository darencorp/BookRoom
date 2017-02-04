angular.module('BookRoomApp')
.controller('HomeCtrl', function($scope, $rootScope, home_service){
    var $this = this;

    $this.openBookForm = function (id)  {
        home_service.getBook(id, function (ret) {
            $rootScope.$emit('showBookForm', ret.data);
        });
    };

    $this.saveMarketBook = function(book) {
        home_service.saveMarketBook(book);
    };

    $this.getBooks = function () {
        home_service.getBooks(function(ret) {
            $this.books = ret.data.books;
        });

        home_service.getLibrary(function (ret)  {
            $this.library = ret.data.library;
        });
    };

    $this.getBooks();

    $this.openUserSetting = function ()  {
        $.UIkit.modal('#user-form').show();
    };

    $rootScope.$on('updateLibrary', function (event, data) {
        $this.library = data;
    });
});