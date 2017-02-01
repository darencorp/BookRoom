angular.module('BookRoomApp')
    .factory('home_service', function ($http) {
       var service = {
           saveMarketBook: function (book, success) {
               $http({method: 'POST', url: $.nano(urls['upload']), data: book, contentType: "multipart/form-data"}).then(success);
           },
           getBooks: function (success) {
               $http({method: 'POST', url: $.nano(urls['home']), contentType: "multipart/form-data"}).then(success);
           },
           getBook: function (id, success) {
               $http({method: 'POST', url: $.nano(urls['book'], {id:id}), contentType: "application/x-www-form-urlencoded"}).then(success);
           }

       };

       return service;
    });