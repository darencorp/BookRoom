angular.module('BookRoomApp')
.controller('BookCtrl', function($scope, $rootScope, $http){

    $scope.processBook = function (id) {
        $http({
            method: 'POST',
            url: $.nano(urls['book-buy'], {id:id}),
            contentType: "application/x-www-form-urlencoded"})
            .then(function (ret) {
                switch (ret.data.status) {
                    case 'ok':
                        $.UIkit.notify("This book has been added to your library.", {status:'success'});
                        $scope.updateLibrary();
                        break;
                    case 'present':
                        $.UIkit.notify('You already have this book.', {status:'warning'});
                        break;
                    case 'error':
                        $.UIkit.notify('This book has been deleted.', {status:'danger'});
                        break;
                    default:
                        break;
                }
        });
    };

    $scope.updateLibrary = function () {
        $http({
            method: 'POST',
            url: $.nano(urls['library']),
            contentType: "application/x-www-form-urlencoded"})
            .then(function (ret) {
                $rootScope.$emit('updateLibrary', ret.data.library);
            }
        );
    };

    $rootScope.$on('showBookForm', function (event, data) {
        $scope.book = data.book;
        $.UIkit.modal('#book-form').show();
    });
});