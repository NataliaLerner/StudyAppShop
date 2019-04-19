import pymysql
import logging
import traceback
import uuid
from datetime import datetime
from flask import session

from .config import DbSettings
from . import log
from .base_type import AccessLevel, User, Category

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




