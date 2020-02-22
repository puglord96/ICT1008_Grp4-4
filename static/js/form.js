 // The first parameter are the coordinates of the center of the map
  // The second parameter is the zoom level
  var map = L.map('map').setView([1.402208, 103.907128], 11);
    L.map('map').setView([1.402208, 103.907128], 11);
  // {s}, {z}, {x} and {y} are placeholders for map tiles
  // {x} and {y} are the x/y of where you are on the map
  // {z} is the zoom level
  // {s} is the subdomain of cartodb
    var layer = L.tileLayer('http://basemaps.cartocdn.com/light_all/11/1.402208/103.907128.png', {
    attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors, &copy; <a href="http://cartodb.com/attributions">CartoDB</a>'
    });

    // Now add the layer onto the map
    map.addLayer(layer);