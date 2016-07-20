
routes.controller('players',['$scope', '$http', '$timeout', function($scope, $http, $timeout){
  $scope.players = {};

  $scope.propertyName = 'name'; // set the default sort type
  $scope.sortReverse  = false;  // set the default sort order

  // PAGINATION
  $scope.totalPlayers = 0;
  $scope.pointer = 0;
  $scope.offset = 0;
  $scope.endIndex = 6;
  $scope.startIndex = 0;


  $scope.range = function(n) {
        if ( n == undefined || n == null || isNaN(n))
            n = 0; 
        return new Array(n);
  };

  $scope.reverse_seasons = function(){

  };

  $scope.nextList = function(){
    if ($scope.pointer < $scope.totalPlayers - 1){
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
    if ($scope.pointer in $scope.players == false)
      fetchData();
  }
  // PAGINATION

  var fetchData = function(){
      $http.get('/players/'+$scope.offset).then(function(response){
        console.log(response);
        var res = response.data;
        var players = res.players;

        $scope.totalPlayers = Math.ceil(res.totalNumberOfPlayers / 10);
        $scope.offset += players.length;
        console.log($scope.pointer);
        $scope.players[$scope.pointer] = [];

        for(var i in players){
          var player = players[i];
          var newPlayer = {
            name: player.name,
            nationality: player.nation,
            position: player.position,
            jerseyNumber: player.jersey_num,
            dateOfBirth: player.birth,
            team: player.team
          };
          $scope.players[$scope.pointer].push(newPlayer);
        }

      });
  };

  fetchData()
}]);