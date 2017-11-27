angular.module('BookRoomApp')
    .factory('home_service', function ($http) {
       var service = {
           // saveMarketBook: function (book, success) {
           //     $http({method: 'POST', url: $.nano(urls['upload']), data: book, contentType: "multipart/form-data"}).then(success);
           // }
       };

       return service;
    });