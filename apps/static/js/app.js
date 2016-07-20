'use strict';

var myApp = angular.module('golazoApp',['ngRoute']);

// myApp.factory('searchBar', function() {
//     return {
//         search: function() {
//             //call search
//         }
//     };
// });

myApp.run(function($rootScope) {
    $rootScope.searchBarArguments = "";
});

var routes = myApp.config(['$httpProvider', function($httpProvider) {
  $httpProvider.defaults.useXDomain = true;
  $httpProvider.defaults.withCredentials = true;
  delete $httpProvider.defaults.headers.common["X-Requested-With"];
  $httpProvider.defaults.headers.common["Accept"] = "application/json";
  $httpProvider.defaults.headers.common["Content-Type"] = "application/json";
}])

.config(["$routeProvider",
  function($routeProvider){
    $routeProvider.
    when('/',{
      templateUrl: '/static/partials/index.html',
      controller: 'main'
    }).
    when('/about',{
      templateUrl: '/static/partials/about.html',
      controller: 'about'
    })
    .when('/games',{
      templateUrl: '/static/partials/games.html',
      controller: 'games'
    })
    .when('/players',{
      templateUrl: '/static/partials/players.html',
      controller: 'players'
    })
    .when('/teams',{
      templateUrl: '/static/partials/teams.html',
      controller: 'teams'
    })
    .when('/games',{
      templateUrl: '/static/partials/games.html',
      controller: 'games'
    })
    .when('/seasons',{
      templateUrl: '/static/partials/seasons.html',
      controller: 'seasons'
    })
    .when('/standings/:id',{
      templateUrl: '/static/partials/standings.html',
      controller: 'standings'
    })
    .when('/team/:id',{
      templateUrl: '/static/partials/team.html',
      controller: 'team'
    })
    .when('/search',{
      templateUrl: '/static/partials/search.html',
      controller: 'search'
    })
    .when('/visual',{
      templateUrl: '/static/partials/visualization.html',
      controller: 'visual'
    })
    .otherwise({redirectTo:'/'})
  }]);

routes.controller('main',['$scope', '$http', '$rootScope', function($scope, $http, $rootScope){
  $scope.games = [];
  $scope.show_card = false;

  if ($scope.games.length <2)
    $scope.show_card = true;
}]);

routes.controller('about',['$scope', '$http', '$timeout', function($scope, $http, $timeout){

  $scope.testOut = '';

  $scope.getTestOutput = function() {
    $http.get('/runtests').then(function(response) {
      var res = response.data;
      $scope.testOut = res;
    });
  };

  $scope.clearTestOutput = function() {
      $scope.testOut = '';
  };


}]);
