from flask import Flask, render_template, session

from core import ListBooks
from core import DbApi
from core import OAuthSignIn, GoogleSignIn


app = Flask(__name__)
app.secret_key = '5e8d527e-7dc4-4be5-8364-44ae3dcb43d0'

@app.route('/')
def index():
	session['shopping'] = {'1':[],'2':[]}

	return render_template('index.html')

@app.route('/shop')
def shop():
	books = [
	ListBooks(link_icon="https://s4-goods.ozstatic.by/480/157/104/104157_0_Kompyuternie_seti_Endryu_Tanenbaum.jpg", name="Компьютерные сети", author="Таненбаум"),
	ListBooks(link_icon="https://s4-goods.ozstatic.by/480/157/104/104157_0_Kompyuternie_seti_Endryu_Tanenbaum.jpg", name="Компьютерные сети", author="Таненбаум"),
	ListBooks(link_icon="https://s4-goods.ozstatic.by/480/157/104/104157_0_Kompyuternie_seti_Endryu_Tanenbaum.jpg", name="Компьютерные сети", author="Таненбаум"),
	ListBooks(link_icon="https://s4-goods.ozstatic.by/480/157/104/104157_0_Kompyuternie_seti_Endryu_Tanenbaum.jpg", name="Компьютерные сети", author="Таненбаум"),
	ListBooks(link_icon="https://s4-goods.ozstatic.by/480/157/104/104157_0_Kompyuternie_seti_Endryu_Tanenbaum.jpg", name="Компьютерные сети", author="Таненбаум"),
	ListBooks(link_icon="https://s4-goods.ozstatic.by/480/157/104/104157_0_Kompyuternie_seti_Endryu_Tanenbaum.jpg", name="Компьютерные сети", author="Таненбаум"),

			]

	count_shop = len(session['shopping'])
	return render_template('shop.html', count_shop = count_shop, books=books)

@app.route('/authorize/<provider>')
def oauth_authorize(provider):
    oauth = OAuthSignIn.get_provider(provider)
    return oauth.authorize()

@app.route('/callback/<provider>')
def oauth_callback(provider):
    oauth = OAuthSignIn.get_provider(provider)
    username, email = oauth.callback()
    return render_template('index.html')

if __name__ == '__main__':
	app.run(debug=True)
