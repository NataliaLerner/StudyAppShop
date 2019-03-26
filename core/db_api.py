import pymysql
import logging

from .config import DbSettings
import core.log

logger = logging.getLogger(__name__)

class DbApi:
	_conn = None
	_cur = None
	_db_settings = None

	def __init__(self):
		self._db_settings = DbSettings()
		self.connection()

	def connection(self):
		try:
			logger.info("Пробуем подключитсься к базе данных {0}, по адресу {1} (порт {2})".format(
				self._db_settings.db_name,self._db_settings.host_name, self._db_settings.port))
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

	def get_books(self, type='1'):
		query = """SELECT * FROM books WHERE '%(type)s'"""%{'type':type}
		self._cur.execute(query)
		self._cur.fetchall()
		return []

