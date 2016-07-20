
routes.controller('teams',['$scope', '$http', '$timeout', function($scope, $http, $timeout){
  $scope.teams = {};

  $scope.propertyName = 'name'; // set the default sort type
  $scope.sortReverse  = false;  // set the default sort order

  // PAGINATION
  $scope.totalTeams = 0;
  $scope.pointer = 0;
  $scope.offset = 0;
  $scope.endIndex = 6;
  $scope.startIndex = 0;

  $scope.range = function(n) {
        return new Array(n);
  };

  $scope.nextList = function(){
    if ($scope.pointer < $scope.totalTeams - 1){
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
    if ($scope.pointer in $scope.teams == false)
      fetchData();
  }
  // PAGINATION

  var fetchData = function(){
      $http.get('/teams/'+$scope.offset).then(function(response){
        console.log(response);
        var res = response.data;
        var teams = res.teams;

        $scope.totalTeams = Math.ceil(res.totalNumberOfTeams / 10);
        $scope.offset += teams.length;
        console.log($scope.pointer);
        $scope.teams[$scope.pointer] = [];

        for(var i in teams){
          var team = teams[i];
          var newTeam = {
            logo:team.logo_url,
            id:team.team_id,
            name:team.team_name,
            shortName:team.nickname,
            squadMarketValue: team.market_val
          };
          $scope.teams[$scope.pointer].push(newTeam);
        }

      });
  };

  fetchData();



}]);