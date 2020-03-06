//For the MapBox API functionality
alert(data[0]);
mapboxgl.accessToken = 'pk.eyJ1IjoianNvbWEiLCJhIjoibFJmYl9JWSJ9.AUm8d76cbOvVEn2mMeG_ZA';
var map = new mapboxgl.Map({
    container: 'map',
    style: 'mapbox://styles/mapbox/streets-v9',
    center: [midArray[1], midArray[0]],
    zoom: 15
});
var test = {"type": "Feature", "geometry": {"type": "Point", "coordinates": [103.8998, 1.4075]}}
console.log(test);
console.log(data);
var d = d.replace("&#39","," );
//var d2 = decodeURI(data);
console.log(d);

map.on('load', function () {
    var geojsonData = {
        "type": "FeatureCollection",
        "features": [
            {
                "type": "Feature",
                "geometry": {
                    "type": "Point",
                    "coordinates": [103.9072, 1.3984]
                }
            },
            {
                "type": "Feature",
                "geometry": {
                    "type": "Point",
                    "coordinates": [103.8984397, 1.4090686]
                }
            },
            {
                "type": "Feature",
                "geometry": {
                    "type": "Point",
                    "coordinates": [103.8998, 1.4075]
                }
            },
            //data

        ]
    };

    map.addSource('route', {
        'type': 'geojson',
        'data': {
            'type': 'Feature',
            'properties': {},
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
            "data": geojsonData
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