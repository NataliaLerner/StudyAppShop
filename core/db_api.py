import pymysql
import logging
import traceback
import uuid
from datetime import datetime
from flask import session

from .config import DbSettings
from . import log
from .base_type import AccessLevel, User, Category, ImageType, ImageGoods, Language, Manufacture, Goods

logger = logging.getLogger(__name__)

class DbApi:
	_conn = None
	_cur = None
	_db_settings = None

	def __init__(self):
		self._db_settings = DbSettings()
		self.connection()

	def connection(self):
		"""
		Подключение к БД, получение курсора
		"""
		try:
			logger.info("Пробуем подключитсься к базе данных {0}, по адресу {1} (порт {2})".format(
				self._db_settings.db_name, self._db_settings.host_name, self._db_settings.port))
			self._conn = pymysql.connect(host=self._db_settings.host_name, port=self._db_settings.port,
				user=self._db_settings.user_name, passwd=self._db_settings.password, 
				db=self._db_settings.db_name)
			logger.info("Успешно подключились к БД!")
		except pymysql.Error as err:
			logger.error("Не удалось подключиться к БД, error: {}".format(err))
		if self._conn:
			try:
				logger.info("Пробуем получить курсор")
				self._cur = self._conn.cursor()
				logger.info("Успешно получили курсор!")
			except pymysql.Error as err:
				logger.error("Не удалось получить курсор, error: {}".format(err))

	def try_except(function):
		def wrapper(*args, **kwargs):
			res = None
			try:
				args[0]._cur = args[0]._conn.cursor()
				res = function(*args, **kwargs)
			except pymysql.Error as err:
				logger.error(err)
			except Exception as e:
				logger.error(traceback.format_exc())
			return res
		return wrapper

	def commit(function):
		def wrapper(*args, **kwargs):
			res = function(*args, **kwargs)
			args[0]._conn.commit()
			args[0]._cur = args[0]._conn.cursor()
			return res
		return wrapper

	def valid_admin(function):
		def wrapper(*args, **kwargs):
			if 'token_user' in session.keys():
				if args[0].is_valid_token(session['token_user']):
					res = function(*args, **kwargs)
					return res
				else:
					raise Exception("Токен, переданный с запросом не валидный!!!")
					return None
			else:
				raise Exception("Токен, переданный с запросом не валидный!!!")
				return None
		return wrapper

	@try_except
	def get_user(self, user_name, e_mail):
		"""
		Получение данных о пользователе из БД, если нет пользователя в БД, создает запись в БД
		"""
		query = """SELECT * FROM Users WHERE e_mail = "{0}" """.format(e_mail)
		logger.info(query)
		self._cur.execute(query)
		res = self._cur.fetchall()
		if len(res) > 0:
			return User(res[0][0], res[0][1], res[0][2], res[0][3], res[0][4])
		else:
			id_ = self.set_user(user_name, e_mail)
			return User(id_, user_name, e_mail, None, AccessLevel.USER)

	@try_except
	@valid_admin
	def get_users(self):
		"""
		to do: добавить фильтры
		"""
		query = "select * from Users"
		self._cur.execute(query)
		users = self._cur.fetchall()
		res = User.ToListUsersNT(users)
		return res


	@try_except
	@valid_admin
	@commit
	def delete_user(self, user_id):
		query = "delete from Users where id = '{0}'".format(user_id)
		logger.info(query)
		self._cur.execute(query)

	@try_except
	@valid_admin
	@commit
	def update_user(self, user_id, access_level):
		pname = 'sp_users_03'
		args = (user_id, access_level)
		status = self._cur.callproc(pname,args)


	@try_except
	@commit
	def set_user(self, user_name, e_mail, access_level = AccessLevel.USER):
		"""
		Добавление нового пользователя в БД
		"""
		query = """INSERT INTO Users(user_name, e_mail, access_level) VALUES ("{0}", "{1}", "{2}")""".format(user_name, e_mail, access_level)
		logger.info(query)
		self._cur.execute(query)
		return self._conn.insert_id()

	@try_except
	@valid_admin
	def get_categories(self, name_filter):
		"""
		селект категорий с фильтром по имени
		"""
		name_filter = "%" + name_filter + "%"
		query = "SELECT * FROM Categories where name like '{0}'".format(name_filter)
		logger.info(query)
		self._cur.execute(query)
		categories = self._cur.fetchall()
		res = Category.ToListCategoryNT(categories)
		return res

	@try_except
	@valid_admin
	def get_goods(self):
		"""
		"""
		query = """SELECT Products.product_id, Products.name, Products.short_name,\
		 Products.description, Products.price, Products.is_available, Products.quantity,\
		  Products.publish_year, Languages.language_id, Languages.name, Languages.short_name,\
		   Manufactures.manufacturer_id, Manufactures.name, Manufactures.short_name, Categories.category_id,\
		    Categories.name, Categories.short_name FROM Products LEFT JOIN Languages ON \
		    Products.language_id = Languages.language_id LEFT JOIN Manufactures ON\
		     Products.manufacturer_id = Manufactures.manufacturer_id LEFT JOIN Categories ON\
		      Products.category_id = Categories.category_id"""
		logger.info(query)
		self._cur.execute(query)
		goods = self._cur.fetchall()
		res = []
		for g in goods:
			language = Language(g[8], g[9], g[10])
			manufacture = Manufacture(g[11], g[12], g[13])
			category = Category(g[14], g[15], g[16])
			temp = Goods(g[0], g[1], g[2], g[3], g[4], g[5], g[6], g[7], language, manufacture, category, self.get_images_for_id_goods(g[0]))
			res.append(temp)
		return res

	@try_except
	@valid_admin
	def get_images_for_id_goods(self, _id):
		"""
		"""
		query = """SELECT Images.image_id, Images.name, Images.short_name,\
		 Images.path, ImageTypes.image_type_id, ImageTypes.desciption FROM\
		  ProductImages LEFT JOIN Images ON ProductImages.image_id = Images.image_id\
		   LEFT JOIN ImageTypes ON Images.image_type_id = ImageTypes.image_type_id WHERE\
		    ProductImages.product_id = {0}""".format(_id)
		logger.info(query)
		self._cur.execute(query)
		images = self._cur.fetchall()
		res = []
		for i in images:
			type_image = ImageType(i[4], i[5])
			image = ImageGoods(i[0], i[1], i[2], i[3], type_image)
			res.append(image)
		return res


	@try_except
	@commit
	def get_token(self, user_id):
		"""
		создание токена, запись в БД
		"""
		token = str(uuid.uuid1())
		query = """CALL CreateToken("{0}", "{1}")""".format(token, user_id)
		logger.info(query)
		self._cur.execute(query)
		return token, datetime.now().strftime("%d.%m.%y %H:%M:%S")

	@try_except
	def get_create_date_token(self, token):
		"""
		получение даты создания токена по токену
		"""
		query = """SELECT token FROM ValidateAdmin WHERE token = '{0}'""".format(token)
		logger.info(query)
		self._cur.execute(query)
		return self._cur.fetchall()[0]

	@try_except
	def is_valid_token(self, token):
		"""
		проверяет наличие токена в БД
		"""
		query = """SELECT * FROM ValidateAdmin WHERE token = '{0}'""".format(token)
		logger.info(query)
		self._cur.execute(query)
		if len(self._cur.fetchall()) > 0:
			return True
		else:
			return False

	@try_except
	@valid_admin
	@commit
	def delete_categories(self, category_id):
		"""
		удаление категории по id
		"""
		query = "delete from Categories where category_id = '{0}'".format(category_id)
		logger.info(query)
		self._cur.execute(query)

	@try_except
	@valid_admin
	@commit
	def create_categories(self, name, short_name):
		"""
		создание новой категории
		ретурн: id созданной категории
		"""
		pname = 'sp_categories_01'
		id = None
		args = (id, name, short_name)
		status = self._cur.callproc(pname,args)
		id = self._cur.fetchone()
		return id[0]

	@try_except
	@valid_admin
	@commit
	def update_categories(self, id, name, short_name):
		pname = 'sp_categories_03'
		args = (id, name, short_name)
		status = self._cur.callproc(pname,args)

	@try_except
	@valid_admin
	def get_map_language(self):
		query = """SELECT name FROM Languages"""
		logger.info(query)
		self._cur.execute(query)
		res = []
		for i in self._cur.fetchall():
			res.append(i[0])
		return res

	@try_except
	@valid_admin
	def get_map_manufacture(self):
		query = """SELECT name FROM Manufactures"""
		logger.info(query)
		self._cur.execute(query)
		res = []
		for i in self._cur.fetchall():
			res.append(i[0])
		return res

	@try_except
	@valid_admin
	def get_map_image_types(self):
		query = """SELECT desciption FROM ImageTypes"""
		logger.info(query)
		self._cur.execute(query)
		res = []
		for i in self._cur.fetchall():
			res.append(i[0])
		return res

	@try_except
	@valid_admin
	def get_map_category(self):
		query = """SELECT name FROM Categories"""
		logger.info(query)
		self._cur.execute(query)
		res = []
		for i in self._cur.fetchall():
			res.append(i[0])
		return res
