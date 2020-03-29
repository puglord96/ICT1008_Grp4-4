from flask_wtf import FlaskForm
from wtforms import SelectField, SubmitField, Label
from wtforms.validators import DataRequired
from pathFind import search
import csv, urllib
import json
#import basehash
MRTLRTStations = []
HDBBlocks = []
latlong = []

geoDict = []
longCoordinates = []

type = "type"

tempstart = (103.9156265, 1.3947758)
tempend = (103.9160709, 1.4031447)
pathArray = search(tempstart, tempend, output="coords")


with open('datasets/Punggol LRT Stations.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')

    for row in csv_reader:
        MRTLRTStations.append((row[0], row[1]))

with open('datasets/punggol-hdb-latlong.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')

    for row in csv_reader:
        HDBBlocks.append((row[0], row[1]))
        coordinates = row[1].split(',')
        lat = coordinates[0]
        long = coordinates[-1]
        newCoordinates = [float(long), float(lat)]
        latlong.append(newCoordinates)




print(latlong)

    #geojsonData = {"type": "Feature", "geometry": {"type": "Point", "coordinates": LL}}
    #geoDict.append(geojsonData)

    # print(g)
geoDict2 = [{type: "Feature", "geometry": {"type": "Point", "coordinates": [103.8998, 1.4075]}}]
#print(geoDict2)
appJson = json.dumps(geoDict2)
#print(appJson)

value = float(103.9128130)
value2 = float(1.4075)




LLTest = [103.8998, 1.4075]


# geojsonData = {"type": "Feature", "geometry": {"type": "Point", "coordinates": latlong}}

class MapForm(FlaskForm):
    BestPathChoice = SelectField('Method of Travel', choices=[(0, 'Choose type of Path...'), ('walk', 'Walking the street'),
                                                               ('bus', 'Bus'),
                                                               ('mrt', 'Mrt')],
                                 validators=[DataRequired()])
    MRTLocation = SelectField('MRT/LRT Station', choices=[(station[0], station[1]) for station in MRTLRTStations],
                              validators=[DataRequired()])
    HDBLocation = SelectField('Destination', choices=[(hdb[1], hdb[0]) for hdb in HDBBlocks],
                              validators=[DataRequired()])
    submit = SubmitField('Find')
