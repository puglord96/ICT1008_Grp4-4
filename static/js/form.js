//For the MapBox API functionality

mapboxgl.accessToken = 'pk.eyJ1IjoicHVnbG9yZDk2IiwiYSI6ImNrN2hjMm5oMzA4eGIzaW4weXFtdHZsaGYifQ._xqaM8Rf9EwMYW-xzqgmBg';
var map = new mapboxgl.Map({
    container: 'map',
    style: 'mapbox://styles/puglord96/ck7hc4ku10yq21ilv13yz3aif',
    center: [midArray[1], midArray[0]],
    zoom: 15
});

function style(feature) {
    return {
        color: '#06406F',
        opacity: 1,
        fillColor: '#DDDDFF',
        fillOpacity: 0.9,
        weight: 3,
        radius: 6,
        clickable: true
    }
}


var arrayLength = data.length;
map.on('load', function () {
    var geojson = {
        "type": "FeatureCollection",
        features: []
    };

    for (var m = 0; m < arrayLength; m++) {
        geojson.features.push({
            "type": "Feature",
            "geometry": {
                //"type": "Point",
                "coordinates": data[m]
            },
        });

    }

    geojson.features.forEach(function (marker) {
        // create a HTML element for each feature
        var el = document.createElement('div');
        el.className = 'marker';
        // make a marker for each feature and add to the map
        new mapboxgl.Marker(el)
            .setLngLat(marker.geometry.coordinates)
            .addTo(map);
    });


    var start = {
        type: 'FeatureCollection',
        features: [{
            type: 'Feature',
            geometry: {
                type: 'Point',
                coordinates: [midArray[1], midArray[0]]
            }
        }]
    };

    start.features.forEach(function(marker) {

  // create a HTML element for each feature
  var el = document.createElement('div');
  el.className = 'marker1';

  // make a marker for each feature and add to the map
  new mapboxgl.Marker(el)
    .setLngLat(marker.geometry.coordinates)
    .addTo(map);
});

     var end = {
        type: 'FeatureCollection',
        features: [{
            type: 'Feature',
            geometry: {
                type: 'Point',
                coordinates: [destArray[1], destArray[0]]
            }
        }]
    };

    end.features.forEach(function(marker) {

  // create a HTML element for each feature
  var el = document.createElement('div');
  el.className = 'marker2';

  // make a marker for each feature and add to the map
  new mapboxgl.Marker(el)
    .setLngLat(marker.geometry.coordinates)
    .addTo(map);
});


    map.addSource('route', {
        'type': 'geojson',
        'data': {
            'type': 'Feature',
            'properties': {color: "#ffffff"},
            'geometry': {
                'type': 'LineString',
                'coordinates': [
                    [103.9072, 1.3984],
                    [103.8984397, 1.4090686],
                    [103.9158001,1.3945725]
                ]
            }
        }
    });


    map.addLayer({
        'id': 'route',
        'type': 'line',
        'source': 'route',
        'layout': {
            'line-join': 'round',
            'line-cap': 'round'
        },
        'paint': {
            'line-color': '#888',
            'line-width': 4
        }
    });


});