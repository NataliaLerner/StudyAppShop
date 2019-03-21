import configparser

class DbSettings:
	_ini_file_name = ''
	_config = None

	def __init__(self, ini_file_name = './../settings/db_settings.ini'):
		self._ini_file_name = ini_file_name
		self.load_ini_file()

	def load_ini_file(self):
		self._config = configparser.ConfigParser()
		self._config.read(self._ini_file_name)

	def save_ini_file(self):
		with open(self._ini_file_name, 'w') as configfile:
			self._config.write(configfile)

	@property
	def user_name(self):
		return self._config['DB_SETTINGS']['user_name']

	@property
	def password(self):
		return self._config['DB_SETTINGS']['password']

	@property
	def host_name(self):
		return self._config['DB_SETTINGS']['host_name']

	@property
	def db_name(self):
		return self._config['DB_SETTINGS']['db_name']

	@property
	def ini_file_name(self):
		return self._ini_file_name

	@property
	def port(self):
		return int(self._config['DB_SETTINGS']['port'])

	@property
	def full_host_name(self):
		return self._config['DB_SETTINGS']['host_name'] + ':' + self._config['DB_SETTINGS']['port']
