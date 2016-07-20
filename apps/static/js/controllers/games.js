

routes.controller('games',['$scope', '$http', '$timeout', function($scope, $http, $timeout){

  $scope.games = {};
  $timeout = twttr.widgets.load();

  $scope.propertyName = 'date'; // set the default sort type
  $scope.sortReverse  = false;  // set the default sort order

  // PAGINATION
  $scope.totalGames = 0;
  $scope.pointer = 0;
  $scope.offset = 0;
  $scope.endIndex = 6;
  $scope.startIndex = 0;

  $scope.range = function(n) {
        return new Array(n);
  };

  $scope.nextList = function(){
    if ($scope.pointer < $scope.totalGames - 1){
      $scope.pointer++;
      $scope.endIndex++;
      $scope.startIndex++;
      $scope.goToPage($scope.pointer);
    }
  }

  $scope.prevList = function(){
    if ($scope.pointer > 0){
      $scope.pointer--;
      $scope.endIndex--;
      $scope.startIndex--;
      $scope.goToPage($scope.pointer);
    }
  }

  $scope.goToPage = function(i){
    $scope.pointer = i;
    $scope.endIndex = $scope.pointer+6;
    $scope.startIndex = $scope.pointer;
    if ($scope.pointer in $scope.games == false)
      fetchData();
  }

  // PAGINATION
  var fetchData = function(){
      $http.get('/games/'+$scope.offset).then(function(response){
        console.log("GAMES");
        console.log(response);
        var res = response.data;
        var games = res.games;

        $scope.totalGames = Math.ceil(res.totalNumberOfGames / 10);
        $scope.offset += games.length;
        $scope.games[$scope.pointer] = [];

        for(var i in games){
          var game = games[i];
          var newGame = {
            date: game.date,
            awayTeamName: game.away_team_name,
            homeTeamName: game.home_team_name,
            home_team_score:game.home_team_score,
            away_team_score: game.away_team_score,
            home_team_id: game.home_team_id, 
            away_team_id: game.away_team_id,
            season: game.season
          };
          $scope.games[$scope.pointer].push(newGame);
        }

      });
  };

  fetchData();

}]);

