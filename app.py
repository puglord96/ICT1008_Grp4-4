from flask import Flask, render_template, request, jsonify, url_for
from form import MapForm, geoDict, geoDict2, LLTest
from config import Config

app = Flask(__name__)

app.config['SECRET_KEY'] = '4cfbdadf2d991953407bb0942aa37e3a'



@app.route('/')
def home_page():
    form = MapForm()
    BestPathChoice = request.args.get('BestPathChoice')
    MRTLRTLocation = request.args.get('MRTLocation')
    HDBLocation = request.args.get('HDBLocation')
    data = geoDict2
    print(geoDict2)

    return render_template('home.html', form=form, methods=['GET'], path=BestPathChoice, station=MRTLRTLocation,
                           hdb=HDBLocation, data=data)



@app.route('/test')
def hello_world():
    return render_template('test.html', title='About')


if __name__ == '__main__':
    app.run(debug=True)
