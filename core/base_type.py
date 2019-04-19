from collections import namedtuple
from enum import IntEnum

ListBooks = namedtuple('listBooks', 'link_icon name author')
CategoryNT = namedtuple('categories', 'category_id name short_name')
UserNT = namedtuple('users', 'user_id name e_mail number_phone access_level')

class AccessLevel(IntEnum):
	ADMIN = 0
	USER = 1

class User:
	_id = None
	_user_name = None
	_e_mail = None
	_number_phone = None
	_access_level = AccessLevel.USER

	def __init__(self, id_ , user_name, e_mail, number_phone, access_level = AccessLevel.USER):
		self._id = id_
		self._user_name = user_name
		self._e_mail = e_mail
		self._number_phone = number_phone
		self._access_level = access_level

	def __str__(self):
		return "User: id={0} , user_name={1} , e_mail={2} , number_phone={3} , access_level={4}".format(
			self._id, self._user_name, self._e_mail, self._number_phone, self._access_level)

	def ToListUsersNT(users):
		res = []
		for user in users:
			res.append(UserNT(user_id = user[0], name = user[1], e_mail = user[2], number_phone = user[3], access_level  = user[4]))
		return res

	def ToMap(users):
		return [{'user_id': k, 'name': v, 'e_mail': e,'number_phone': u, 'access_level': l} for k, v, e, u, l in users]


class Book:
	__id = None
	__descr = None

	def __init__(self):
		pass

	def toListBooks(self):
		pass

class Category:

	__category_id = None
	__name = None
	__short_name = None

	def __init__(self, category_id, name, short_name):
		self.__id = category_id
		self.__name = name
		self.__short_name = short_name

	def ToListCategoryNT(categories):
		res = []
		for category in categories:
			res.append(CategoryNT(category_id=category[0], name=category[1], short_name=category[2]))
		return res

	def ToMap(categories):
		return [{'category_id': k, 'name': v, 'short_name': e} for k,v,e in categories]

	def __str__(self):
		return "id={0} , name={1} , short_name={2}".format(
			self.__category_id, self.__name, self.__short_name)