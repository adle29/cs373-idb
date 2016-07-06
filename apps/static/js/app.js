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
    });
  };

  var fetchTeam = function(team_id){
    $http.get('/team/'+id).then(function(response){
      var res = response.data;
      console.log(res);
      $scope.team = {
        name:res.name,
        logo:res.crestUrl,
        shortName: res.shortName,
        squadMarketValue: res.squadMarketValue
      };
    });
  };

  fetchTeam(id);
  fetchGames(id);
  fetchPlayers(id);

}]);

routes.controller('standings',['$scope', '$http', '$routeParams', function($scope, $http, $routeParams){
  var id = $routeParams.id;

  //# change route to '/season/'+id later
  $http.get('/data/season_'+id+".json").then(function(response){

    var res = response.data;
    var standings;
    var matchDay = res.matchday;

    $scope.leagueCaption = res.leagueCaption;
    $scope.matchDay = res.matchday;
    $scope.numberOfMatches = res.numberOfMatchdays;
    $scope.numberOfGames = res.numberOfGames;
    $scope.completed = $scope.numberOfMatches == $scope.matchDay;
    $scope.groups = [];

    if( $scope.matchDay == 1 || $scope.completed ) {
      $scope.seasonFinished = true;
      var standings = res.standing;

      var group = {
        letter: 'A',
        teams: []
      };

      for (var i in standings){
        var team = standings[i];
        if (team["team"] != ""){

          var newTeam = {
            logo:team["crestURI"],
            name:team["team"],
            id:team["teamId"],
            rank:team["rank"],
            playedGames: team["playedGames"],
            goalsAgainst: team["goalsAgainst"],
            goals: team["goals"],
            pts: team["points"]
          };
          group.teams.push(newTeam);
        }
      }

      $scope.groups.push(group);
    }
    else {
      var standings = res.standings;

      console.log(res);

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

  //later change to url = /seasons
  $http.get('/data/seasons.json').then(function(response){
    console.log(response);
    var res = response.data;
    for (var i = 0; i < res.length; i++) {
        var element = res[i];
        var season = {
          name: element.caption,
          league: element.league,
          numberOfTeams: element.numberOfTeams,
          numberOfGames: element.numberOfGames,
          numberOfMatchdays: element.numberOfMatchdays,
          currentMatchday: element.currentMatchday,
          completed: element.currentMatchday == element.numberOfMatchdays,
          id: element.id,
          year: element.year
        };
        $scope.seasons.push(season);
    }
  });

}]);

routes.controller('games',['$scope', '$http', '$timeout', function($scope, $http, $timeout){
  $scope.games = [];
  $timeout = twttr.widgets.load();

  $http.get('/data/game.json').then(function(response){
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

routes.controller('players',['$scope', '$http', '$timeout', function($scope, $http, $timeout){
  $scope.games = [];
  $http.get('/data/players.json').then(function(response){
    console.log(response);
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
}]);

routes.controller('teams',['$scope', '$http', '$timeout', function($scope, $http, $timeout){

  $http.get('/data/teams.json').then(function(response){
    console.log(response);
    var res = response.data;
    $scope.teams = [];

    for (var i in res) {
      var team = res[i];

      var newTeam = {
        logo:team.crestUrl,
        id:team.id,
        name:team.name,
        shortName:team.shortName,
        squadMarketValue: team.squadMarketValue
      };

      $scope.teams.push(newTeam);
    }

  });
}]);
