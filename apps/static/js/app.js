'use strict';

var myApp = angular.module('golazoApp',['ngRoute']);

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
  $http.get('/season/'+id+'/standings').then(function(response){

    console.log(response);
    var res = response.data;
    var seasonData = res.season;
    var standings;

    $scope.leagueCaption = seasonData.season_name;
    $scope.matchDay = seasonData.cur_match_day;
    $scope.numberOfMatches = seasonData.num_match_days;
    $scope.numberOfGames = seasonData.num_games;
    $scope.completed = seasonData.numberOfMatches == $scope.matchDay;
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
            id:team["team_id"],
            rank:team["rank"],
            playedGames: team["playedGames"],
            goalsAgainst: team["goals_against"],
            goals: team["goals_for"],
            pts: team["points"]
          };
          group.teams.push(newTeam);
        }
      }

      $scope.groups.push(group);
    }
    else {
      var standings = res.standings;

      console.log("many groups");

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
            id:team.team_id,
            rank:String(team.rank).trim(),
            playedGames: team.playedGames,
            goalsAgainst: team.goals_against,
            goals: team.goals_for,
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

  $scope.seasons = {};
  $scope.propertyName = 'name'; // set the default sort type
  $scope.sortReverse  = false;  // set the default sort order
  $scope.totalSeasons = 0;
  $scope.pointer = 0;
  $scope.offset = 0;

  $scope.range = function(n) {
        return new Array(n);
  };

  $scope.nextList = function(){
    if ($scope.pointer < $scope.totalSeasons - 1){
      $scope.pointer++;
      $scope.goToPage($scope.pointer);
    }
  }

  $scope.prevList = function(){
    if ($scope.pointer > 0){
      $scope.pointer--;
      $scope.goToPage($scope.pointer);
    }
  }

  $scope.goToPage = function(i){
    $scope.pointer = i;

    if ($scope.pointer in $scope.seasons == false){
      fetchData();
    }
  }

  //later change to url = /seasons
  var fetchData = function(){
    $http.get('/seasons/'+$scope.offset).then(function(response){
      console.log(response);
      var res = response.data;
      var seasons = res.seasons;

      $scope.totalSeasons = Math.ceil(res.totalNumberOfSeasons / 10);
      $scope.offset += seasons.length;
      console.log($scope.pointer);
      $scope.seasons[$scope.pointer] = [];

      for (var i = 0; i < seasons.length; i++) {
          var element = seasons[i];
          var season = {
            name: element.season_name,
            league: element.league,
            numberOfTeams: element.num_teams,
            numberOfGames: element.num_games,
            numberOfMatchdays: element.num_match_days,
            currentMatchday: element.cur_match_day,
            completed: element.cur_match_day == element.num_match_days,
            id: element.season_id,
            year: element.year
          };
          $scope.seasons[$scope.pointer].push(season);
      }
    });
  }

  fetchData();

}]);

routes.controller('games',['$scope', '$http', '$timeout', function($scope, $http, $timeout){
  $scope.games = [];
  $timeout = twttr.widgets.load();

  $scope.propertyName = 'date'; // set the default sort type
  $scope.sortReverse  = false;  // set the default sort order

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

  $scope.propertyName = 'name'; // set the default sort type
  $scope.sortReverse  = false;  // set the default sort order

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

  $scope.propertyName = 'name'; // set the default sort type
  $scope.sortReverse  = false;  // set the default sort order

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
