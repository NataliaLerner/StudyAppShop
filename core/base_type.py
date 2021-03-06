from collections import namedtuple
from enum import IntEnum

DEFAULT_ADDRES = "http://127.0.0.1:3306"

ListBooks = namedtuple('listBooks', 'id link_icon name author description price quantity year category')
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

class Goods:
	_id 			= None
	_full_name 		= None
	_short_name 	= None
	_descr 			= None
	_price 			= None
	_available 		= False
	_count 			= None
	_year 			= None
	_language 		= None
	_manufacture 	= None
	_category 		= None
	_images 		= []

	def __init__(self, _id, full_name, short_name, descr, price, available, count, year, 
		language, manufacture, category, images = []):
		self._id 			=  _id
		self._full_name 	= full_name
		self._short_name 	= short_name
		self._descr 		= descr
		self._price 		= price
		self._available 	= available
		self._count 		= count
		self._year 			= year
		self._language 		= language
		self._manufacture 	= manufacture
		self._category 		= category
		self._images 		= images

	def to_dict(self):
		res = {}
		res['_id'] 			= self._id
		res['_full_name'] 	= self._full_name
		res['_short_name'] 	= self._short_name
		res['_descr'] 		= self._descr
		res['_price'] 		= self._price
		res['_available'] 	= self._available
		res['_count'] 		= self._count
		res['_year'] 		= self._year
		res['_language'] 	= self._language.to_dict()
		res['_manufacture'] = self._manufacture.to_dict()
		res['_category'] 	= self._category.to_dict()
		res['_images'] 		= []
		for i in self._images:
			res['_images'].append(i.to_dict())
		return res
		#res = self.__dict__
		#print(self._language)
		#res['_language'] = self._language.__dict__
		#res['_manufacture'] = self._manufacture.__dict__
		#res['_category'] = self._category.__dict__
		#for i in range(len(res['_images'])):
		#	res['_images'][i] = self._images[i].__dict__
		#	res['_images'][i]['_image_type'] = self._images[i]['_image_type'].__dict__

	def ToMap(goods):
		for i in goods:
			print(i.to_dict())
		return [ a.to_dict() for a in goods]

class Language:
	_id = None 
	_name = None
	_short_name = None

	def __init__(self, _id, name, short_name):
		self._id = _id
		self._name = name
		self._short_name = short_name

	def to_dict(self):
		res = {}
		res['_id'] 			= self._id
		res['_name'] 		= self._name
		res['_short_name'] 	= self._short_name
		return res

class Manufacture:
	_id = None 
	_name = None
	_short_name = None

	def __init__(self, _id, name, short_name):
		self._id = _id
		self._name = name
		self._short_name = short_name

	def to_dict(self):
		res = {}
		res['_id'] 			= self._id
		res['_name'] 		= self._name
		res['_short_name'] 	= self._short_name
		return res

class ImageGoods:
	_id = None
	_name = None
	_short_name = None
	_path = None
	_image_type = None

	def __init__(self, _id, name, short_name, path, image_type):
		self._id = _id
		self._name = name
		self._short_name = short_name
		self._path = path
		self._image_type = image_type

	def to_dict(self):
		res = {}
		res['_id'] 			= self._id
		res['_name'] 		= self._name
		res['_short_name'] 	= self._short_name
		res['_path'] 		= self._path
		res['_image_type'] 	= self._image_type.to_dict()
		return res

class ImageType:
	_id = None
	_descr = None

	def __init__(self, _id, descr):
		self._id = _id
		self._descr = descr

	def to_dict(self):
		res = {}
		res['_id'] 			= self._id
		res['_descr'] 		= self._descr
		return res


class Category:

	__category_id = None
	__name = None
	__short_name = None

	def __init__(self, category_id, name, short_name):
		self.__id = category_id
		self.__name = name
		self.__short_name = short_name

	def to_dict(self):
		res = {}
		res['_id'] 			= self.__id
		res['_name'] 		= self.__name
		res['_short_name'] 	= self.__short_name
		return res

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