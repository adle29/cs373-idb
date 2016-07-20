// var myApp = angular.module('golazoApp',['ngRoute']);

// myApp.run(function($rootScope) {
//     $rootScope.searchBarArguments = "";
// });

// var routes = myApp.config(['$httpProvider', function($httpProvider) {
//   $httpProvider.defaults.useXDomain = true;
//   $httpProvider.defaults.withCredentials = true;
//   delete $httpProvider.defaults.headers.common["X-Requested-With"];
//   $httpProvider.defaults.headers.common["Accept"] = "application/json";
//   $httpProvider.defaults.headers.common["Content-Type"] = "application/json";
// }])


routes.controller('search',['$scope', '$http', '$rootScope', function($scope, $http, $rootScope){

  $scope.searchKeys = $rootScope.searchBarArguments; 
  $scope.seasons = []; 
  $scope.games = []; 
  $scope.players = []; 
  $scope.teams = []; 
  $scope.loading = false; 

  console.log($rootScope.searchBarArguments);

  $scope.query_search = function(){
    $scope.seasons = []; 
    $scope.games = []; 
    $scope.players = []; 
    $scope.teams = []; 
    $scope.loading = true; 

    if ($scope.searchKeys != ""){
      var parameters = $scope.searchKeys;
      parameters = parameters.replace(/\w\S*/g, function(txt){return txt.charAt(0).toUpperCase() + txt.substr(1).toLowerCase();});
      parameters = parameters.replace(" ", "%20");

      console.log(parameters);
      if (parameters.length > 0 && parameters != undefined ){
        $http.get('/search?q='+parameters).then(function(response){
          $scope.loading = false; 
          var res = response.data; 
          console.log(res);
          var seasons = res.seasons; 
          var players = res.players; 
          var teams = res.teams; 
          var games = res.games; 

          for(var i in seasons){
            var season = seasons[i];
            var newSeason =  {
              season_name: season.season_name,
              id: season.season_id
            };

            $scope.seasons.push(newSeason);

          }

          for(var i in teams){
            var team = teams[i];
            var newTeam =  {
              name: team.team_name,
              id: team.team_id
            };

            $scope.teams.push(newTeam);

          }

          for(var i in players){
            var player = players[i];
            var newPlayer =  {
              name: player.name,
              team_id: player.team_id
            };

            $scope.players.push(newPlayer);

          }

          for(var i in games){
            var game = games[i];
            var newGame =  {
              away_team: game.away_team_name,
              home_team: game.home_team_name,
              season_id: game.season_id
            };

            $scope.games.push(newGame);
          }



        }); 

        console.log($scope.games);
      }
    } //end if

    else {
       $scope.loading = false; 
    }

  };

  $scope.query_search();

}]);
