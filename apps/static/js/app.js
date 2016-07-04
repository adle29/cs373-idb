'use strict';

var myApp = angular.module('golazoApp',['ngRoute'])

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
      templateUrl: '/static/partials/about.html'
    })
    .when('/games',{
      templateUrl: '/static/partials/games.html',
      controller: 'games'
    })
    .when('/seasons',{
      templateUrl: '/static/partials/seasons.html',
      controller: 'seasons'
    })
    .when('/season/:id',{
      templateUrl: '/static/partials/season.html',
      controller: 'season'
    })
    .when('/team/:id',{
      templateUrl: '/static/partials/team.html',
      controller: 'team'
    })
    .otherwise({redirectTo:'/'})
  }]);

routes.controller('main',['$scope', '$http',function($scope, $http){
  $scope.games = [];
  $scope.show_card = false;

  $http.get('/games').then(function(response){
    console.log(response);
    var res = response.data.fixtures;
    for (var i = 0; i < res.length; i++) {
        var element = res[i];
        var game = {
          date: element.date,
          awayTeamName: element.awayTeamName,
          homeTeamName: element.homeTeamName
        };
        $scope.games.push(game);
    }
  });

  if ($scope.games.length <2)
    $scope.show_card = true;
}]);

routes.controller('team',['$scope', '$http', '$routeParams', function($scope, $http, $routeParams){
  var id = $routeParams.id;

  var fetchPlayers = function(team_id){
    $http.get("/team/"+team_id+"/players").then(function(response){
       var res = response.data;
       var players = res.players;
       $scope.players = [];

       for(var i in players){
         var player = players[i];
         var newPlayer = {
           name: player.name,
           nationality: player.nationality,
           position: player.position,
           jerseyNumber: player.jerseyNumber,
           dateOfBirth: player.dateOfBirth
         };
         $scope.players.push(newPlayer);
       }

   });
  };

  var fetchGames = function(team_id){
    $http.get("/team/"+team_id+"/fixtures").then(function(response){
      console.log(response.data);

      var res = response.data;
      var games = res.fixtures;
      $scope.games = [];

      for(var i in games){
        var game = games[i];
        var newGame = {
          matchday: game.matchday,
          awayTeamName: game.awayTeamName,
          homeTeamName: game.homeTeamName,
          date: game.date,
          id: game.id
        };
        $scope.games.push(newGame);
      }
      console.log($scope.games);
    });
  };

  var fetchTeam = function(team_id){
    $http.get('/team/'+id).then(function(response){
      var res = response.data;
      $scope.team = {
        name:res.name,
        logo:res.crestUrl
      };
    });
  };

  fetchTeam(id);
  fetchGames(id);
  fetchPlayers(id);

}]);

routes.controller('season',['$scope', '$http', '$routeParams', function($scope, $http, $routeParams){
  var id = $routeParams.id;

  $http.get('/season/'+id).then(function(response){

    var res = response.data;

    console.log(res);
    var standings;
    var matchDay = res.matchday;

    $scope.leagueCaption = res.leagueCaption;
    $scope.groups = [];

    console.log( matchDay );

    if( matchDay == 1 ) {
      var standings = res.standing;

      var group = {
        letter: 'A',
        teams: []
      };

      console.log(standings);

      for (var i in standings){
        var team = standings[i];
        if (team["team"] != ""){

          var newTeam = {
            logo:team["crestURI"],
            name:team["team"],
            id:team["teamId"],
            rank:team["rank"]
          };
          group.teams.push(newTeam);
        }
      }

      $scope.groups.push(group);
    }
    else {
      var standings = res.standings;
      for (var groupLetter in standings) {

        var rawGroupData = standings[groupLetter];
        var group = {
          letter: String(groupLetter).trim(),
          teams: []
        };

        for (var i in rawGroupData) {
          var team = rawGroupData[i];

          var newTeam = {
            logo:team.crestURI,
            name:team.team,
            id:team.teamId,
            rank:String(team.rank).trim(),
            playedGames: team.playedGames,
            goalsAgainst: team.goalsAgainst,
            goals: team.goals,
            pts: team.points

          };

          group.teams.push(newTeam);
        }

        $scope.groups.push(group);
      }
    }

  });

}]);


routes.controller('seasons',['$scope', '$http', function($scope, $http){

  $scope.seasons = [];

  $http.get('/seasons').then(function(response){
    console.log(response);
    var res = response.data;
    for (var i = 0; i < res.length; i++) {
        var element = res[i];
        var season = {
          name: element.caption,
          league: element.league,
          id: element.id,
          year: element.year
        };
        $scope.seasons.push(season);
    }
  });

}]);

routes.controller('games',['$scope', '$http', function($scope, $http){
  $scope.games = [];

  $http.get('/games').then(function(response){
    console.log(response);
    var res = response.data.fixtures;
    for (var i = 0; i < res.length; i++) {
        var element = res[i];
        var game = {
          date: element.date,
          awayTeamName: element.awayTeamName,
          homeTeamName: element.homeTeamName
        };
        $scope.games.push(game);
    }
    console.log($scope.games);
  });
}]);
