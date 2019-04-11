from collections import namedtuple
from enum import IntEnum

ListBooks = namedtuple('listBooks', 'link_icon name author')
CategoryNT = namedtuple('categories', 'category_id name short_name')

class AccessLevel(IntEnum):
	ADMIN = 0
	USER = 1

class User:
	_id = None
	_user_name = None
	_e_mail = None
	_number_phone = None
	_access_level = AccessLevel.USER

	def __init__(self, id_ , user_name, e_mail, number_phone, access_lavel = AccessLevel.USER):
		self._id = id_
		self._user_name = user_name
		self._e_mail = e_mail
		self._number_phone = number_phone
		self._access_lavel = access_lavel

	def __str__(self):
		return "User: id={0} , user_name={1} , e_mail={2} , number_phone={3} , access_level={4}".format(
			self._id, self._user_name, self._e_mail, self._number_phone, self._access_level)


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

	def CreateCategory(self):
		pass

	def UpdateCategory(self):
		pass

	def DeleteCategory(self):
		pass

	def ToListCategory(categories):
		res = []
		for category in categories:
			res.append(Category(category_id=category[0], name=category[1], short_name=category[2]))
		return res


	def ToList(categories):
		res =[]
		for category in categories:
			temp = Category(category_id = category[0], name=category[1], short_name=category[2])
			res.append(temp)
		return res

	#To named tuple
	def ToCategoryNT(self):
		return CategoryNT(category_id=self.__category_id, name=self.__name, short_name=self.__short_name)

	def ToListCategoryNT(categories):
		res = []
		for category in categories:
			res.append(CategoryNT(category_id=category[0], name=category[1], short_name=category[2]))
		return res

	def __str__(self):
		return "id={0} , name={1} , short_name={2}".format(
			self.__category_id, self.__name, self.__short_name)