from flask import Flask,render_template
from flask_wtf import FlaskForm

app = Flask(__name__)


posts = [
    {
        'author': 'KS the great',
        'title': 'Fastest Route from MRT to HDB flat',
        'content': 'Fastest Route Map',
        'date_posted': 'April 12, 1997'
    },
{
        'author': 'KS the awesome',
        'title': 'Cheapest Route from MRT to HDB flat',
        'content': 'Cheapest Route Map',
        'date_posted': 'April 12, 1997'
    }
]


@app.route('/')
def text_msg():
    return render_template('home.html', posts=posts)


@app.route('/test')
def hello_world():
    return render_template('test.html', title='About')




if __name__ == '__main__':
    app.run()



