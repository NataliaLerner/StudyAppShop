from flask import Flask, render_template, session


app = Flask(__name__)
app.secret_key = '5e8d527e-7dc4-4be5-8364-44ae3dcb43d0'


@app.route('/')
def hello_world():
	session['shopping'] = {'1':[],'2':[]}
	return render_template('index.html')

@app.route('/shop')
def shop():
	count_shop = len(session['shopping'])
	return render_template('shop.html', count_shop = count_shop)
