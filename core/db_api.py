import pymysql
import logging
import traceback

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

	@try_except
	def get_user(self, user_name, e_mail):
		"""
		Получение данных о пользователе из БД, если нет пользователя в БД, создает запись в БД
		"""
		query = """SELECT * FROM Users WHERE user_name = "{0}" AND e_mail = "{1}" """.format(user_name, e_mail)
		logger.info(query)
		self._cur.execute(query)
		res = self._cur.fetchall()
		if len(res) > 0:
			return User(res[0][0], res[0][1], res[0][2], res[0][3], res[0][4])
		else:
			id_ = self.set_user(user_name, e_mail)
			return User(id_, user_name, e_mail, None, AccessLevel.USER)

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
	def get_categories(self, name_filter):
		"""
		"""
		name_filter = "%" + name_filter + "%"
		query = "SELECT * FROM Categories where name like '{0}'".format(name_filter)
		logger.info(query)
		self._cur.execute(query)
		categories = self._cur.fetchall()
		res = Category.ToListCategoryNT(categories)
		return res

