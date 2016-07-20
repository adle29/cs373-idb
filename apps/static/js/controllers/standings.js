
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
    $scope.completed = $scope.numberOfMatches == $scope.matchDay;
    $scope.groups = [];

    console.log("Completed: " + $scope.completed, $scope.numberOfMatches, $scope.matchDay);

    if( $scope.matchDay == 1 || $scope.completed ) {
      $scope.seasonFinished = true;
      var standings = res.standings;

      var group = {
        letter: 'A',
        teams: []
      };

      for (var i in standings){
        var team = standings[i];
        if (team["team"] != ""){

          var newTeam = {
            logo:team["logo_url"],
            name:team["team_name"],
            id:team["team_id"],
            rank:team["rank"],
            playedGames: team["matches_played"],
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

        console.log(rawGroupData);

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
      console.log($scope.groups);
    }

  });

}]);
