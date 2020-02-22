from flask_wtf import FlaskForm
from wtforms import SelectField, StringField
from wtforms.validators import DataRequired, Length
import csv, urllib


MRTLRTStations = []
HDBBlocks = []

with open('datasets/Punggol LRT Stations.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')

    for row in csv_reader:
        MRTLRTStations.append((row[0], row[1]))

with open('datasets/hdb-property-information.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')

    for row in csv_reader:
        HDBBlocks.append((row[0],row[0]))
print(HDBBlocks)


class MapForm(FlaskForm):
    BestPathChoice = SelectField(u'Type of Best Path', choices=[('fast', 'Fastest Route'), ('short', 'Shortest Route')])
    MRTLocation = SelectField(u'MRT/LRT Station', choices=[(station[0], station[1]) for station in MRTLRTStations])
