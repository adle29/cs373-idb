var ForceDirectedVisual = function(graph, mixedData, idCharacters){
  
  var svg = d3.select("svg"),
      width = $("svg").parent().width(),//svg.attr("width"),
      height = $("svg").parent().height();//svg.attr("height");

  var color = d3.scaleOrdinal(d3.schemeCategory20);
  var BOUNDS = 0.4
  var simulation = d3.forceSimulation()
      .force("link", d3.forceLink().id(function(d) { return d.id; }))
      .force("charge", d3.forceManyBody())
      .force("x", d3.forceX().strength(BOUNDS))
      .force("y", d3.forceY().strength(BOUNDS))
      .force("center", d3.forceCenter(width / 3, height / 2));

  var link = svg.append("g")
      .attr("class", "links")
    .selectAll("line")
    .data(graph.links)
    .enter().append("line")
      .attr("stroke-width", function(d) { return 1; });


      
  var node = svg.append("g")
      .attr("class", "nodes")
    .selectAll("circle")
    .data(graph.nodes)
    .enter().append("circle")
      .attr("r", 3)
      .attr("fill", function(d) { return color(d.group); })

      .on("click", function(d){
         if( d.type == "house"){
             var name = d.name;
             console.log(color(d.group));
             var text = "<div class='insideDiv'><h3 style=' color:"+ color(d.group) +";'>" +d.name + "</h3><ul>";

             var members = mixedData[d.name];

             console.log(d.name, members);

             for(var i = 0; i < members.length; i++){
                var memberID = members[i];
                text += "<li><small>"+idCharacters[memberID] + "</small></li>";
             }  

             var legend = svg.select("#legend");

             text += "<lu></div>"

             legend.html(text);

             // var div = legend.append('xhtml:div')
             //            .append('div').append('p').html(text);

         }

      })
      .call(d3.drag()
          .on("start", dragstarted)
          .on("drag", dragged)
          .on("end", dragended));

  node.append("text")
    .text(function(d) { return d.name; });


  var texts = svg.selectAll("text.label")
            .data(graph.nodes)
            .enter().append("text")
            .attr("class", "label")
            .attr("fill", function(d){
              if (d.type == "house")
                return color(d.group);
              else
                return "black";
            })
            .attr("font-size", "8px")
            .attr("visibility", function(d){
              if (d.type == "house")
                return "visible";
              else
                return "hidden";
            })
            .text(function(d) {  return d.name;  });


    svg.append("foreignObject")
        .attr("id", "legend")
        .attr("width", "300px")
        .attr("height", "700px")
        .style("border", "solid black 1px")
        .attr("x", ($("svg").parent().width() - 450) + "px")
        .attr("y", "30px").html("Click a house to display its members.");

   var control = svg.append("foreignObject")
      .attr("id", "control")
      .attr("x", "30px")
      .attr("y", "30px");

  simulation
      .nodes(graph.nodes)
      .on("tick", ticked);

  simulation.force("link")
      .links(graph.links);


  var html = '<input name="updateButton" class="btn" type="button" value="Zoom +" onclick="zoomPlus()" /><input name="updateButton" class="btn" type="button"  value="Zoom -" onclick="zoomMinus()" />';

  control.append('xhtml:div').append("input")
    .attr("class", "btn")
    .attr("value", "ZOOM -")
    .style("float", "left")
    .style("margin", "10px")
    .attr("type","button")
    .on("click", function(){
      zoomPlus();
    });

  control.append('xhtml:div').append("input")
    .attr("class", "btn")
    .attr("value", "ZOOM +")
    .style("margin", "10px")
    .attr("type","button")
    .on("click", function(){
      zoomMinus();
    });


  function zoomPlus(){
    BOUNDS += 0.1;
    simulation.force("x", d3.forceX().strength(BOUNDS))
              .force("y", d3.forceY().strength(BOUNDS));
    console.log("click");
  }
  
  function zoomMinus(){
    BOUNDS -= 0.1;
    simulation.force("x", d3.forceX().strength(BOUNDS))
              .force("y", d3.forceY().strength(BOUNDS));
  }

  function ticked() {
    link
        .attr("x1", function(d) { return d.source.x; })
        .attr("y1", function(d) { return d.source.y; })
        .attr("x2", function(d) { return d.target.x; })
        .attr("y2", function(d) { return d.target.y; });

    node
        .attr("cx", function(d) { return d.x; })
        .attr("cy", function(d) { return d.y; });

    texts.attr("transform", function(d) {
        return "translate(" + d.x + "," + d.y + ")";
    });
  }

  function dragstarted(d) {
    if (!d3.event.active) simulation.alphaTarget(0.3).restart();
    d.fx = d.x;
    d.fy = d.y;
  }

  function dragged(d) {
    d.fx = d3.event.x;
    d.fy = d3.event.y;
  }

  function dragended(d) {
    if (!d3.event.active) simulation.alphaTarget(0);
    d.fx = null;
    d.fy = null;
  }

};