from flask import Flask, request, make_response

app = Flask(__name__)


@app.route('/')
def index():
    return "<h3> this is a basic flask page </h3>"

@app.route('/hello')
def hello():
    return "hello world"


@app.route('/greet/<name>',methods=['GET','POST'])
def greet(name):
    if request.method=='GET':
        return f'{name} this is a get request\n'
    elif request.method=='POST':
        return f'{name} this a post request\n'
    else:
        return "i will find you and kill you\n"
    return f"hi i am {name}"

@app.route('/basic')
def basic():
    #return 'hello\n',201
    response= make_response('HOPATEROCKSTAR5STAR')
    response.status_code=202
    response.headers['content-type']='stream KARMA'
    return response

@app.route('/add/<int:a>/<int:b>')
def add(a,b):
    return f'{a}+{b}={a+b}'

@app.route('/handle_url_params')
def handle_parms():
    if 'greeting' in request.args.keys() and 'name' in request.args.keys():
        greeting= request.args['greeting']
        name= request.args.get('name')
        return f'{greeting},{name}'
    else:
        return 'Some parameters are missing'

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)