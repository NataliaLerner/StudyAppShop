from collections import namedtuple
from enum import IntEnum

ListBooks = namedtuple('listBooks', 'link_icon name author')

class AccessLavel(IntEnum):
	ADMIN = 0
	USER = 1

class User:
	_id = None
	_user_name = None
	_e_mail = None
	_number_phone = None
	_access_lavel = AccessLavel.USER

	def __init__(self, id_ , user_name, e_mail, number_phone, access_lavel = AccessLavel.USER):
		self._id = id_
		self._user_name = user_name
		self._e_mail = e_mail
		self._number_phone = number_phone
		self.access_lavel = access_lavel

	def __str__(self):
		return "User: id={0} , user_name={1} , e_mail={2} , number_phone={3} , access_lavel={4}".format(
			self._id, self._user_name, self._e_mail, self._number_phone, self._access_lavel)


class Book:

	def __init__(self):
		pass

	def toListBooks(self):
		pass
