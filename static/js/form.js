//For the MapBox API functionality

mapboxgl.accessToken = 'pk.eyJ1IjoianNvbWEiLCJhIjoibFJmYl9JWSJ9.AUm8d76cbOvVEn2mMeG_ZA';
var map = new mapboxgl.Map({
    container: 'map',
    style: 'mapbox://styles/mapbox/streets-v9',
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

    for (var m = 0; m < arrayLength; m++){

    geojson.features.push({
        "type": "Feature",
        "geometry":{
            //"type": "Point",
            "coordinates": data[m]
        },
    });

    }

   geojson.features.forEach(function(marker) {
        // create a HTML element for each feature
      var el = document.createElement('div');
      el.className = 'marker';
      // make a marker for each feature and add to the map
      new mapboxgl.Marker(el)
        .setLngLat(marker.geometry.coordinates)
        .addTo(map);
    });

    map.addSource('route', {
        'type': 'geojson',
        'data': {
            'type': 'Feature',
            'properties': {color:"#ffffff"},
            'geometry': {
                'type': 'LineString',
                'coordinates': [
                    [103.9072, 1.3984],
                    [103.8984397, 1.4090686]
                ]
            }
        }
    });
    map.addLayer({
        "id": "points",
        "type": "circle",
        "source": {
            "type": "geojson",
            "data": geojson
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