from flask import Flask, render_template, session, redirect, url_for, request

from core import ListBooks, Category
from core import DbApi
from core import OAuthSignIn, GoogleSignIn
import json

import os, ssl
if (not os.environ.get('PYTHONHTTPSVERIFY', '') and
        getattr(ssl, '_create_unverified_context', None)):
    ssl._create_default_https_context = ssl._create_unverified_context

app = Flask(__name__)

@app.route('/')
def index():
    session['shopping'] = {'1':[],'2':[]}
    return render_template('index.html', show = False)

@app.route('/contacts')
def contacts():
    return render_template('contacts.html')

@app.route('/basket')
def basket():
    return render_template('basket.html', e1=0)

@app.route('/get_token')
def test():
    pass

@app.route('/shop')
def shop():
    books = [
    ListBooks(link_icon="https://s4-goods.ozstatic.by/480/157/104/104157_0_Kompyuternie_seti_Endryu_Tanenbaum.jpg", name="Компьютерные сети", author="Таненбаум"),
    ListBooks(link_icon="https://s4-goods.ozstatic.by/480/157/104/104157_0_Kompyuternie_seti_Endryu_Tanenbaum.jpg", name="Компьютерные сети", author="Таненбаум"),
    ListBooks(link_icon="https://s4-goods.ozstatic.by/480/157/104/104157_0_Kompyuternie_seti_Endryu_Tanenbaum.jpg", name="Компьютерные сети", author="Таненбаум"),
    ListBooks(link_icon="https://s4-goods.ozstatic.by/480/157/104/104157_0_Kompyuternie_seti_Endryu_Tanenbaum.jpg", name="Компьютерные сети", author="Таненбаум"),
    ListBooks(link_icon="https://s4-goods.ozstatic.by/480/157/104/104157_0_Kompyuternie_seti_Endryu_Tanenbaum.jpg", name="Компьютерные сети", author="Таненбаум"),
    ListBooks(link_icon="https://s4-goods.ozstatic.by/480/157/104/104157_0_Kompyuternie_seti_Endryu_Tanenbaum.jpg", name="Компьютерные сети", author="Таненбаум"),
    ListBooks(link_icon="https://s4-goods.ozstatic.by/480/157/104/104157_0_Kompyuternie_seti_Endryu_Tanenbaum.jpg", name="Компьютерные сети", author="Таненбаум"),
    ListBooks(link_icon="https://s4-goods.ozstatic.by/480/157/104/104157_0_Kompyuternie_seti_Endryu_Tanenbaum.jpg", name="Компьютерные сети", author="Таненбаум"),
    ListBooks(link_icon="https://s4-goods.ozstatic.by/480/157/104/104157_0_Kompyuternie_seti_Endryu_Tanenbaum.jpg", name="Компьютерные сети", author="Таненбаум"),
    ListBooks(link_icon="https://s4-goods.ozstatic.by/480/157/104/104157_0_Kompyuternie_seti_Endryu_Tanenbaum.jpg", name="Компьютерные сети", author="Таненбаум"),
    ListBooks(link_icon="https://s4-goods.ozstatic.by/480/157/104/104157_0_Kompyuternie_seti_Endryu_Tanenbaum.jpg", name="Компьютерные сети", author="Таненбаум"),
    ListBooks(link_icon="https://s4-goods.ozstatic.by/480/157/104/104157_0_Kompyuternie_seti_Endryu_Tanenbaum.jpg", name="Компьютерные сети", author="Таненбаум"),
    ListBooks(link_icon="https://s4-goods.ozstatic.by/480/157/104/104157_0_Kompyuternie_seti_Endryu_Tanenbaum.jpg", name="Компьютерные сети", author="Таненбаум"),
    ListBooks(link_icon="https://s4-goods.ozstatic.by/480/157/104/104157_0_Kompyuternie_seti_Endryu_Tanenbaum.jpg", name="Компьютерные сети", author="Таненбаум"),

    ]
    count_shop = len(session['shopping'])
    return render_template('shop.html', count_shop = count_shop, books=books)

@app.route('/admin')
def admin():
    return render_template('admin.html')

@app.route('/order_management')
def order_management():
    #global db
    #c = db.get_categories("")
    return render_template('order_management.html')

@app.route('/category_management')
def category_management():
    global db
    c = db.get_categories("")
    return render_template('category_management.html', categories = json.dumps(
        [{'category_id': k, 'name': v, 'short_name': e} for k,v,e in c], indent=4))

@app.route('/authorize/<provider>')
def oauth_authorize(provider):
    oauth = OAuthSignIn.get_provider(provider)
    return oauth.authorize()

@app.route('/callback/<provider>')
def oauth_callback(provider):
    global db
    oauth = OAuthSignIn.get_provider(provider)
    username, email = oauth.callback()
    user = db.get_user(username, email)
    session['user'] = user.__dict__
    return redirect('/')

@app.route('/logout')
def logout():
    if 'user' in session.keys():
        session.pop('user')
    return redirect('/')

@app.route('/show_info_card', methods=['GET'])
def show_info_card():
    print(request.args.get('show'))
    return redirect('/')#render_template('index.html', show = True if request.args.get('show') == 'False' else False)

if __name__ == '__main__':
    app.secret_key = '5e8d527e-7dc4-4be5-8364-44ae3dcb43d0'
    db = DbApi()
    app.run(debug=True, port = 3306)
