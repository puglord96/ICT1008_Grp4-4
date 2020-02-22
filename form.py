from flask_wtf import FlaskForm
from wtforms import SelectField, SubmitField,Label
from wtforms.validators import DataRequired
import csv, urllib

MRTLRTStations = []
HDBBlocks = []

with open('datasets/Punggol LRT Stations.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')

    for row in csv_reader:
        MRTLRTStations.append((row[0], row[1]))

with open('datasets/punggol-hdb-latlong.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')

    for row in csv_reader:
        HDBBlocks.append((row[0], row[1].split(",")))


class MapForm(FlaskForm):
    BestPathChoice = SelectField('Type of Best Path', choices=[('fast', 'Fastest Route'), ('short', 'Shortest Route')],
                                 validators=[DataRequired()])
    MRTLocation = SelectField('MRT/LRT Station', choices=[(station[0], station[1]) for station in MRTLRTStations],
                              validators=[DataRequired()])
    HDBLocation = SelectField('Destination', choices=[(hdb[1], hdb[0]) for hdb in HDBBlocks],
                              validators=[DataRequired()])
    submit = SubmitField('Find')
