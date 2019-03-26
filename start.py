from flask import Flask, render_template, session

from core import ListBooks
from core import DbApi


app = Flask(__name__)
app.secret_key = '5e8d527e-7dc4-4be5-8364-44ae3dcb43d0'

db = DbApi()
@app.route('/')
def hello_world():
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
