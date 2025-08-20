from flask import Flask , request, render_template , redirect , url_for , jsonify

app=Flask(__name__)


@app.route('/')
def index():
    return "this is home"

@app.route('/greet/<name>')
def greet(name):
    return f'hello {name}'

@app.route('/success/<int:score>')
def success(score):
    return f'You passed with {score}'

@app.route('/fail/<int:score>')
def fail(score):
    return f'You failed with {score}'

@app.route('/form',methods=["GET","POST"])
def form():
    if request.method=="GET":
        return render_template('form.html')
    else:
        maths=float(request.form['maths'])
        science = float(request.form['science'])
        history = float(request.form['history'])

        avg_marks=(maths+science+history)/3
        res=""
        if avg_marks>50:
            res="success"
        else:
            res="fail"

        return redirect(url_for(res,score=avg_marks))

        #return render_template('form.html', score=avg_marks)

@app.route('/api',methods=["POST"])
def calculate_sum():
    data=request.get_json()
    a_val=float(dict(data)['a'])
    b_val = float(dict(data)['b'])
    return jsonify(a_val+b_val)

if __name__=="__main__":
    app.run(debug=True)