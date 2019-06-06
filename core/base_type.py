from collections import namedtuple
from enum import IntEnum

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


class Statuses:
	_status_id = None
	_descr = None
	_short_descr = None

	def __init__(self, status_id, descr, short_descr):
		self._status_id = status_id
		self._descr = descr
		self._short_descr = short_descr

	def ToList(statuses):
		res = []
		for status in statuses:
			res.append(Statuses(status[0],status[1],status[2]))
		return res

	def ToMap(statuses):
		return [{'status_id': k, 'descr': v, 'short_name': e} for k,v,e in statuses]


class Requests:
	_request_id 		= None
	_status_id 			= None
	_status_descr 		= None
	_customer_name 		= None
	_customer_email 	= None
	_customer_phone 	= None

	def __init__(self,request_id,status_id,status_descr,customer_name,customer_email,customer_phone):
		self._request_id				= request_id
		self._status_id					= status_id
		self._status_descr				= status_descr
		self._customer_name				= customer_name
		self._customer_email			= customer_email
		self._customer_phone 			= customer_phone

	def ToMap(self):
		res = {}
		res['request_id'] 		= self._request_id
		res['status_id'] 		= self._status_id
		res['status_descr'] 	= self._status_descr
		res['customer_name'] 	= self._customer_name
		res['customer_email'] 	= self._customer_email
		res['customer_phone'] 	= self._customer_phone
		return res

	def ToArrOfMap(arr):
		res = []
		for item in arr:
			res.append((Requests(item[0],item[1],item[2], item[3], item[4], item[5])).ToMap())
		return res


class RequestProducts:
	_request_id		= None
	_product_id		= None
	_quantity		= None
	_prod_descr		= None
	_man_descr		= None
	_price			= None

	def __init__(self,_request_id,_product_id,_quantity,_prod_descr,_man_descr,_price):
		self._request_id		= _request_id
		self._product_id		= _product_id
		self._quantity			= _quantity
		self._prod_descr		= _prod_descr
		self._man_descr			= _man_descr
		self._price				= _price


	def ToMap(self):
		res = {}
		res['request_id']	= self._request_id
		res['product_id']	= self._product_id
		res['quantity']		= self._quantity
		res['prod_descr']	= self._prod_descr
		res['man_descr']	= self._man_descr
		res['price']		= self._price
		return res

	def ToArrOfMap(arr):
		res = []
		for item in arr:
			res.append((RequestProducts(item[0],item[1],item[2], item[3], item[4], item[5])).ToMap())
		return res

