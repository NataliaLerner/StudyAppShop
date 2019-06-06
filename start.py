from flask import Flask, render_template, session, redirect, url_for, request
from flask_uploads import UploadSet, configure_uploads, IMAGES
from datetime import datetime

from core import ListBooks, Category, User, Goods
from core import DbApi
from core import OAuthSignIn, GoogleSignIn
from core import DEFAULT_ADDRES
import json
import ast


import os, ssl

if (not os.environ.get('PYTHONHTTPSVERIFY', '') and
        getattr(ssl, '_create_unverified_context', None)):
    ssl._create_default_https_context = ssl._create_unverified_context

app = Flask(__name__)
app.secret_key = '5e8d527e-7dc4-4be5-8364-44ae3dcb43d0'
photos = UploadSet('photos', IMAGES)

app.config['UPLOADED_PHOTOS_DEST'] = 'static/img'
configure_uploads(app, photos)

@app.route('/')
def index():
    session['shopping'] = {'1':[],'2':[]}
    return render_template('index.html', show = False)

@app.route('/contacts')
def contacts():
    return render_template('contacts.html')

@app.route('/basket')
def basket():
    session["basket"] = [{"id_": 1, "count":10}, {"id_": 2, "count":20}]
    global db
    basket_ = []
    if ("basket" in session.keys()):            
        for i in session["basket"]:
            basket_.append(db.get_product_name_and_price(i["id_"]))
            basket_[-1]["count"] = i["count"]

    return render_template('basket.html', basket_ = json.dumps(basket_, indent=4))



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

@app.route('/basket_goods')
def basket_goods():
    return render_template('basket_goods.html')

@app.route('/order_management')
def order_management():
    global db
    requests = db.get_requests()
    statuses = db.get_statuses()
    return render_template('order_management.html',requests = json.dumps(requests, indent=4), statuses = json.dumps(statuses, indent=4))


@app.route('/admin/api/requests/get_additional_info', methods=['POST'])
def get_additional_info():
    global db
    request_id = request.json['request_id']
    request_products = db.get_request_products(request_id)
    print (request_products)
    return json.dumps(request_products, indent=4), 200

@app.route('/admin/api/requests/update_order_status', methods=['POST'])
def update_order_status():
    global db
    request_id = request.json[0]['request_id']
    status_id = request.json[1]['status_id']
    db.update_order_status(request_id,status_id)
    return json.dumps({'result': True})



@app.route('/category_management')
def category_management():
    global db
    c = db.get_categories("")
    return render_template('category_management.html', categories = json.dumps(Category.ToMap(c), indent=4))

@app.route('/management_of_goods')
def management_of_goods():
    global db
    g = db.get_goods()
    js = Goods.ToMap(g)
    l = db.get_map_language()
    m = db.get_map_manufacture()
    c = db.get_map_category()
    i_t = db.get_map_image_types()
    print(l)
    return render_template('management_of_goods.html', goods = json.dumps(js, indent=4), \
        language = json.dumps(l, indent=4), manufacture = json.dumps(m, indent=4),
        category = json.dumps(c, indent=4), image_types = json.dumps(i_t, indent=4))

@app.route('/upload', methods=['POST'])
def upload():
    print(request.files)
    if request.method == 'POST' and 'img' in request.files:
        filename = photos.save(request.files['img'])
        print(DEFAULT_ADDRES + "/static/img/" + filename)
    return DEFAULT_ADDRES + "/static/img/" + filename
    
@app.route('/admin/api/categories/create', methods=['POST'])
def create_category():
    global db
    name = request.json[0]['name']
    short_name = request.json[1]['short_name']
    id = db.create_categories(name, short_name)
    return json.dumps({'category_id': id}), 200

@app.route('/admin/api/image_goods/create', methods=['POST'])
def create_image():
    global db
    print(request.json)
    id2 = request.json[0]['_name']
    id3 = request.json[1]['_short_name']
    id4 = request.json[2]['_path']
    id5 = request.json[3]['_image_type_descr']
    print(id2)
    print(id3)
    print(id4)
    print(id5)
    return json.dumps({'result': True})

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

@app.route('/admin/api/image_goods/update', methods=['POST'])
def update_image():
    global db
    id1 = request.json[0]['_id']
    id2 = request.json[1]['_name']
    id3 = request.json[2]['_short_name']
    id4 = request.json[3]['_path']
    id5 = request.json[4]['_image_type_descr']
    print(request.json)
    print(id1)
    print(id2)
    print(id3)
    print(id4)
    print(id5)
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
    try:
        session['user'] = user.__dict__
        session['token_user'], session['token_datatime'] = db.get_token(session['user']['_id'])
    except:
        print('Ошибка подключения к ББ!')
        return "DB ERROR"
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

@app.errorhandler(404)
def pagenotfound(error):
    return render_template('error404.html'), 404

if __name__ == '__main__':

    db = DbApi()
    app.run(debug=True, port = 3306)
