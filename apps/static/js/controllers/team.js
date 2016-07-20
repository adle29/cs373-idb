routes.controller('team',['$scope', '$http', '$routeParams', function($scope, $http, $routeParams){
  var id = $routeParams.id;

  var fetchPlayers = function(team_id){
    $http.get("/team/"+team_id+"/players").then(function(response){
       var players = response.data;
       console.log(response);
       $scope.players = [];

       for(var i in players){
         var player = players[i];
         var newPlayer = {
           name: player.name,
           nationality: player.nation,
           position: player.position,
           jerseyNumber: player.jersey_num,
           dateOfBirth: player.birth
         };
         $scope.players.push(newPlayer);
       }

   });
  };

  var fetchGames = function(team_id){
    $http.get("/team/"+team_id+"/games").then(function(response){

      var games = response.data;
      $scope.games = [];
       console.log("GAMES");
      console.log(games);

      for(var i in games){
        var game = games[i];
        var newGame = {
          matchday: game.match_day,
          away_team_name: game.away_team_name,
          home_team_name: game.home_team_name,
          home_team_score:game.home_team_score,
          away_team_score: game.away_team_score,
          date: game.date,
          id: game.id,
          season: game.season
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
        name:res.team_name,
        logo:res.logo_url,
        shortName: res.nickname,
        squadMarketValue: res.market_val
      };
    });
  };

  fetchTeam(id);
  fetchGames(id);
  fetchPlayers(id);

}]);