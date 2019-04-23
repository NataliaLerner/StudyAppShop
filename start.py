from flask import Flask, render_template, session, redirect, url_for, request
from datetime import datetime

from core import ListBooks, Category, User, Goods
from core import DbApi
from core import OAuthSignIn, GoogleSignIn
import json
import ast


import os, ssl

if (not os.environ.get('PYTHONHTTPSVERIFY', '') and
        getattr(ssl, '_create_unverified_context', None)):
    ssl._create_default_https_context = ssl._create_unverified_context

app = Flask(__name__)
app.secret_key = '5e8d527e-7dc4-4be5-8364-44ae3dcb43d0'

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
    global db
    if ('user' in session.keys()):
        then = datetime.strptime(session['token_datatime'], "%d.%m.%y %H:%M:%S")
        data = datetime.now() - then
        if data.seconds > 900:
            session['token_user'], session['token_datatime'] = db.get_token(session['user']['_id'])
            print(session['token_user'], session['token_datatime'])
    return ""

@app.route('/shop')
def shop():
    books = [
    ListBooks(id=1,link_icon="https://s4-goods.ozstatic.by/480/157/104/104157_0_Kompyuternie_seti_Endryu_Tanenbaum.jpg", name="Компьютерные сети1", author="Таненбаум", description="blablabla", price="123", quantity="15", year="1812", category="Фантастика"),
    ListBooks(id=2,link_icon="https://s4-goods.ozstatic.by/480/157/104/104157_0_Kompyuternie_seti_Endryu_Tanenbaum.jpg", name="Компьютерные сети2", author="Таненбаум", description="фартук в масле оливье", price="262", quantity="88", year="1990", category="Поэзия"),
    ListBooks(id=3,link_icon="https://s4-goods.ozstatic.by/480/157/104/104157_0_Kompyuternie_seti_Endryu_Tanenbaum.jpg", name="Компьютерные сети3", author="Таненбаум", description="овадлдчижрии", price="3446", quantity="34754", year="2002", category="Детские"),
    ListBooks(id=4,link_icon="https://s4-goods.ozstatic.by/480/157/104/104157_0_Kompyuternie_seti_Endryu_Tanenbaum.jpg", name="Компьютерные сети4", author="Таненбаум", description="Мы идем в тишине по убитой весне", price="46", quantity="1", year="1492", category="Приключения"),
    ListBooks(id=5,link_icon="https://s4-goods.ozstatic.by/480/157/104/104157_0_Kompyuternie_seti_Endryu_Tanenbaum.jpg", name="Компьютерные сети5", author="Таненбаум", description="Во имя Костикова, ИП и святого Романенкова", price="666", quantity="15", year="1", category="Религия"),
    ListBooks(id=6,link_icon="https://s4-goods.ozstatic.by/480/157/104/104157_0_Kompyuternie_seti_Endryu_Tanenbaum.jpg", name="Компьютерные сети6", author="Таненбаум", description="Самосвал песка", price="1488", quantity="15", year="2020", category="Хоррор"),

            ]
    count_shop = len(session['shopping'])
    return render_template('shop.html', count_shop = count_shop, books=books)

@app.route('/admin')
def admin():
    return render_template('admin.html')

@app.route('/order_management')
def order_management():
    #global db
    return render_template('order_management.html')

@app.route('/category_management')
def category_management():
    global db
    c = db.get_categories("")
    return render_template('category_management.html', categories = json.dumps(Category.ToMap(c), indent=4))

@app.route('/management_of_goods')
def management_of_goods():
    global db
    g = db.get_goods()
    print(g)
    js = Goods.ToMap(g)
    print(js)
    return render_template('management_of_goods.html', goods = json.dumps(js, indent=4))

@app.route('/admin/api/categories/create', methods=['POST'])
def create_category():
    global db
    name = request.json[0]['name']
    short_name = request.json[1]['short_name']
    id = db.create_categories(name, short_name)
    return json.dumps({'category_id': id}), 200

@app.route('/admin/api/categories/update', methods=['POST'])
def update_category():
    global db
    id = request.json[0]['category_id']
    name = request.json[1]['name']
    short_name = request.json[2]['short_name']
    db.update_categories(id, name, short_name)
    return json.dumps({'result': True})

@app.route('/admin/api/categories/delete', methods=['POST'])
def delete_category():
    global db
    category_id = request.json['category_id']
    r = db.delete_categories(category_id)
    return json.dumps({'result': True})

@app.route('/users_management')
def users_management():
    global db
    u = db.get_users()
    return render_template('users_management.html', users = json.dumps(User.ToMap(u), indent=4))

@app.route('/admin/api/users/update', methods=['POST'])
def update_user():
    global db
    id = request.json[0]['user_id']
    access = request.json[1]['access_level']
    u = db.update_user(id, access)
    return json.dumps({'result': True})


@app.route('/admin/api/users/delete', methods=['POST'])
def delete_user():
    global db
    user_id = request.json['user_id']
    r = db.delete_user(user_id)
    return json.dumps({'result': True})


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
    session['token_user'], session['token_datatime'] = db.get_token(session['user']['_id'])
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

@app.route('/book/<int:bookid>/<string:bookname>')
def bookinfo(bookid, bookname):
    #select from db where id=bookid
    bbb = books[bookid-1]
    return render_template('bookinfo.html', book = bbb)

@app.errorhandler(404)
def pagenotfound(error):
    return render_template('error404.html'), 404

if __name__ == '__main__':

    db = DbApi()
    app.run(host="0.0.0.0", debug=True, port = 8080)
