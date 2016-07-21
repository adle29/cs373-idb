routes.controller('visual',['$scope', '$http', '$rootScope', function($scope, $http, $rootScope){


	// houses
	// characters
	//events

	//make characters link to houses, houses link to events 
	var urlCharacters = "/static/js/data/characters.json";
	var urlHouses = "/static/js/data/houses.json";

	$scope.characters = []; 
	$scope.houses = []; 

	var model = {};

	var jsonData = { "nodes": [], "links": [] };

	//make the id in houses a link 

	function getRandomArbitrary(min, max) {
	    return Math.random() * (max - min) + min;
	}

	$http.get(urlHouses).then(function(res1){
		$http.get(urlCharacters).then(function(res2){
          var houses = res1.data;
          var characters =  res2.data; 

          console.log(houses[0]); 
          console.log(characters[0]); 

          var colors = {};

          for(var i = 0; i < houses.length; i++){
          	var house = houses[i];
          	var newNode = { "id":house.name, "group": i};
    
          	jsonData["nodes"].push(newNode)

          	var swornMembers = house.swornMembers; 

          	for(var j = 0; j < swornMembers.length; j++){
          		colors[swornMembers[j]] = i;
  				var newLink = {"source":house.name, "target": swornMembers[j], "value": getRandomArbitrary(1, 9), "name":house.name, "type":"house"};
  				jsonData["links"].push(newLink);
  			} //small for

      	  } //end big for

      	  for(var i = 0; i < characters.length; i++){
      	  	var character = characters[i];
          	var newNode = { "id":character.id, "group": colors[character.id], "name":character.name, "type":"character"};
          	jsonData["nodes"].push(newNode);
      	  }

      	  console.log(jsonData);

      	  ForceDirectedVisual(jsonData);
        });               
    });


	// var jsonData = {
	// 	  "nodes": [
	// 	    {"id": "Myriel", "group": 1},
	// 	    {"id": "Napoleon", "group": 1},
	// 	    {"id": "Mlle.Baptistine", "group": 1},
	// 	    {"id": "Mme.Magloire", "group": 1},
	// 	    {"id": "CountessdeLo", "group": 1},
	// 	    {"id": "Geborand", "group": 1},
	// 	    {"id": "Champtercier", "group": 1},
	// 	    {"id": "Cravatte", "group": 1},
	// 	    {"id": "Count", "group": 1},
	// 	    {"id": "OldMan", "group": 1},
	// 	    {"id": "Labarre", "group": 2},
	// 	    {"id": "Valjean", "group": 2},
	// 	    {"id": "Marguerite", "group": 3}

	// 	    ],
	// 	  "links": [
	// 	  	{"source": "Napoleon", "target": "Myriel", "value": 1}
 //    	]};

  //   var myFlower = new ForceDirectedVisual();
		// myFlower.update(jsonData);
		
	// { 
	// 	node: {
	// 		name: house of this
	// 		link: character1
	// 		link: character2
	// 		link: fight
	// 	}

	// 	node: {
	// 		name: fight of something
	// 		link: house of this
	// 		link: house of that
	// 	}
	// }
  



}]);