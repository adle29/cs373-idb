routes.controller('visual',['$scope', '$http', '$rootScope', function($scope, $http, $rootScope){

	var urlCharacters = "/static/js/data/characters.json";
	var urlHouses = "/static/js/data/houses.json";

	$scope.characters = []; 
	$scope.houses = []; 
	$scope.data = {};

	$scope.mixedData = {};
	$scope.idCharacters = {};
	$scope.clickId = "here";

	var model = {};

	var jsonData = { "nodes": [], "links": [] };

	//make the id in houses a link 

	function getRandomArbitrary(min, max) {
	    return Math.random() * (max - min) + min;
	}

	function isInArray(value, array) {
	  return array.indexOf(value) > -1;
	}


	$http.get(urlHouses).then(function(res1){
		$http.get(urlCharacters).then(function(res2){
          var houses = res1.data;
          var characters =  res2.data; 
          $scope.characters = characters; 
		  $scope.houses = houses; 
          console.log(houses[0]); 
          console.log(characters[0]); 

          var colors = {};
          var doNotIncludeCharacters = [];

           for(var i = 0; i < characters.length; i++){
      	  	var character = characters[i];
      	  	if (character.name == ""){
      	  		doNotIncludeCharacters.push( parseInt(character.id) );
      	  	}
      	  }

          for(var i = 0; i < houses.length; i++){
          	var house = houses[i];
          	var newNode = { "id":house.name, "group": i, "name": house.name.slice(6), "type":"house"};
    		
          	jsonData["nodes"].push(newNode)

          	var swornMembers = house.swornMembers; 

          	$scope.mixedData[house.name.slice(6)] = swornMembers;

          	for(var j = 0; j < swornMembers.length; j++){
          		colors[swornMembers[j]] = i;
          		if ( isInArray(parseInt(swornMembers[j]), doNotIncludeCharacters) == false ) {
  					var newLink = {"source":house.name, "target": swornMembers[j], "value": getRandomArbitrary(1, 9), "name":house.name.slice(6)};
  					jsonData["links"].push(newLink);
  				}
  			} //small for

      	  } //end big for

      	  for(var i = 0; i < characters.length; i++){
      	  	var character = characters[i];
      	  	if ( isInArray( parseInt(character.id), doNotIncludeCharacters) == false ) {
      	  		$scope.idCharacters[character.id] = character.name;
          		var newNode = { "id":character.id, "group": colors[character.id], "name":character.name, "type":"character"};
          		jsonData["nodes"].push(newNode);
          	}
      	  }


      	  ForceDirectedVisual(jsonData, $scope.mixedData, $scope.idCharacters);
      	  $scope.data = JSON.stringify(jsonData, null, 2);
        });               
    });






}]);