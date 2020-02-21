from flask import Flask,render_template

app = Flask(__name__)

bootstrap = {
    'stylesheet' : '<link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.4.1/css/bootstrap.min.css" '
                   'integrity="sha384-Vkoo8x4CGsO3+Hhxv8T/Q5PaXtkKtu6ug5TOeNV6gBiFeWPGFN9MuhOf23Q9Ifjh" crossorigin="anonymous">',
    'jquery' : '<script src="https://code.jquery.com/jquery-3.4.1.slim.min.js" '
               'integrity="sha384-J6qa4849blE2+poT4WnyKhv5vZF5SrPo0iEjwBvKU7imGFAV0wwj1yYfoRSJoZ+n" crossorigin="anonymous"></script>',
}

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
    return render_template('home.html',posts=posts)


@app.route('/hello')
def hello_world():
    return 'Hello World!'




if __name__ == '__main__':
    app.run()



