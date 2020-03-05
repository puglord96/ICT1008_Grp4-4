from flask import Flask, render_template, request, jsonify, url_for
from form import MapForm
from config import Config

app = Flask(__name__)

app.config['SECRET_KEY'] = '4cfbdadf2d991953407bb0942aa37e3a'



@app.route('/')
def home_page():
    form = MapForm()
    arr = [];
    BestPathChoice = request.args.get('BestPathChoice')
    MRTLRTLocation = request.args.get('MRTLocation')
    HDBLocation = request.args.get('HDBLocation')

    return render_template('home.html', form=form, methods=['GET'], path=BestPathChoice, station=MRTLRTLocation,
                           hdb=HDBLocation,array = arr)



@app.route('/test')
def hello_world():
    return render_template('test.html', title='About')


if __name__ == '__main__':
    app.run()
