routes.controller('seasons',['$scope', '$http', function($scope, $http){

  $scope.seasons = {};
  $scope.propertyName = 'year'; // set the default sort type
  $scope.sortReverse  = false;  // set the default sort order
  $scope.totalSeasons = 0;
  $scope.pointer = 0;
  $scope.offset = 0;
  $scope.endIndex = 6;
  $scope.startIndex = 0;
  var LIMIT = 10; 

  //search variables

  $scope.range = function(n) {
        if ( n == undefined || n == null || isNaN(n))
            n = 0; 
        return new Array(n);
  };

  $scope.reverse_seasons = function(){

  };

  $scope.nextList = function(){
    if ($scope.pointer < $scope.totalSeasons - 1){
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
    if ($scope.pointer in $scope.seasons == false)
      fetchData();
  }

  //later change to url = /seasons
  var fetchData = function(){

    $http.get('/seasons/'+$scope.pointer*LIMIT).then(function(response){
      console.log(response);
      var res = response.data;
      var seasons = res.seasons;
      console.log($scope.pointer*LIMIT);
      $scope.totalSeasons = Math.ceil(res.totalNumberOfSeasons / 10);
      $scope.offset += seasons.length;
      $scope.seasons[$scope.pointer] = [];

      seasons = seasons.slice(0);

      console.log("HERE");
      console.log(seasons);
          
      seasons.sort(function(a,b) {
          return a.year - b.year;
      })

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


      console.log($scope.seasons);
    });
  }; 

  $scope.query_search = function(){ 
      $scope.cacheSeasons = $scope.seasons; 
      $scope.cacheTotalSeasons = $scope.totalSeasons; 
      $scope.seasons = {};
      $scope.loading = true; 

      if ($scope.searchKeys != ""){
        var parameters = $scope.searchKeys;
            parameters = parameters.replace(/\w\S*/g, function(txt){return txt.charAt(0).toUpperCase() + txt.substr(1).toLowerCase();});
            parameters = parameters.replace(" ", "%20");

        if (parameters.length > 0 && parameters != undefined ){
          $http.get('/search?q='+parameters).then(function(response){
            $scope.loading = false; 
            var res = response.data; 
            console.log(res);
            var seasons = res.seasons; 

            $scope.totalSeasons = Math.ceil(res.totalNumberOfSeasons / 10);
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

                if(i%10 == 0) {
                  $scope.pointer++;
                  $scope.seasons[$scope.pointer] = [];
                }
            }

            console.log($scope.seasons);

          }); 

        }
      } //end if

      else {
         $scope.loading = false; 
      }

  };//finished function 

  fetchData();

}]);