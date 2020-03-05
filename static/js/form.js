
//For the MapBox API functionality
mapboxgl.accessToken = 'pk.eyJ1IjoianNvbWEiLCJhIjoibFJmYl9JWSJ9.AUm8d76cbOvVEn2mMeG_ZA';
  var map = new mapboxgl.Map({
    container: 'map',
    style: 'mapbox://styles/mapbox/streets-v9',
    center:[103.9072,1.3984],
    zoom : 15
  });
  map.on('load', function() {
    var geojsonData = {
      "type": "FeatureCollection",
      "features": [
      {
        "type": "Feature",
        "geometry": {
          "type": "Point",
          "coordinates": [103.9072,1.3984]
        }
      },
      {
        "type": "Feature",
        "geometry": {
          "type": "Point",
          "coordinates": [103.8984397,1.4090686]
        }
      }
      ]
    };
    map.addLayer({
      "id": "points",
      "type": "circle",
      "source": {
        "type": "geojson",
        "data": geojsonData
      }
    })
  });

