# not yet useful
# still working 

import re
from update import update

class URI:

	def __init__(self, arg):
			# the address will be handled as variable 'uri'
			self.uri = arg

			# list of supported network protocols
			# in this script, word 'protocol' will refer to any of this list
			self.protocols = ['http','https','view-source']

			# default(Configurable) network-protocol or if protocol not specified
			self.default = 'http'

			# dictionary of key-value pairs for all informations about address
			self.data = {'scheme':'','host':'','port':None,'path':'','query':{},'hash':'','domain':''}

			# parsing the 'uri' argument
			self.parser(arg)

	def parser(self,arg):

		# checks, if argument(as URI) is 'str' type or not
		if(str(type(arg)) == "<type 'str'>"):



			""" parse and store key-value pairs(if, everything correct) or raise Exception, about type of error """

			""" first attempts, for protocol type of 'uri' """

			
			# when protocol is not defined
			if(self.uri.find('://') == -1):

				# if, 'host' starts from 'www.' ['www.example.com']
				if(self.uri[:4] == 'www.'):

					# add default network-protocol
					self.uri = self.default + '://' + self.uri

					# set 'scheme' to 'http'(default) in list 'data'
					self.data['scheme'] = self.default

				# if, 'host' not starts from 'www' ['example.com']
				else:

					# add deafult network-protocol and add 'www.' in 'host'
					self.uri = self.default + '://www.' + self.uri

					# set 'scheme' to 'http'(default) in list 'data'
					self.data['scheme'] = self.default

			# if protocol is defined and is a valid protocol[exists in the 'protocols' list]
			elif(self.uri[:(self.uri.find('://'))] in self.protocols):

				# adds that valid protocol to list 'data'
				part = self.uri.find('://')
				self.data['scheme'] = self.uri[:part]

				# if, 'host' starts from 'www.'
				if(self.uri[part+3:part+7] == 'www.'):
					# do nothing
					pass
					
				# if, 'host' does't starts from 'www.'
				else:
					# insert 'www.' in between 'scheme' and remaining 
					self.uri = self.data['scheme'] + '://www.' + self.uri[part+3:]

			# raise Exception...if protocol is invalid(not supported)
			else:
				raise Exception("The protocol you defined, is invalid")


			# bulk regex is coming
			# print self.uri

			a = self.uri.find('www')
			r = re.match(r'^(www(\.([a-z]+\-{0,1}[a-z]+)){2,})((\:\d{1,4}){0,1})((\/[a-z]*)||(\/[a-z]+)+\/{0,1})(\?[a-z]\=[a-z](\&[a-z]=[a-z])*){0,1}(\#[a-z]+){0,1}$',self.uri[a:])

			if(r):
				print 'it seems like matching !!'
				print r.groups()

				# adding 'host' value
				self.data['host'] = r.group(1)

				# adding 'domain' value
				self.data['domain'] = r.group(3)

				# no 'port' there
				if(r.group(4) == ''):
					#self.data['port'] = None
					pass

				# 'port' is there...adding it
				else:
					self.data['port'] = int(r.group(4)[1:]) 

				# don't have 'path'
				if(r.group(6) == ''):
					# self.data['path'] = ''
					pass

				# 'path' is there...adding it
				else:
					self.data['path'] = r.group(6)

				# no 'query' thing there
				if(r.group(9) == None):
					pass

				# 'query' is there
				else:

					# converting query's string to 'dict'
					q_sample = r.group(9)[1:]
					sepration = q_sample.split('&')

					for x in sepration:

						eq = x.find('=')
						# adding key-value pairs for 'query'
						self.data['query'][x[:eq]] = x[eq+1:]

				# 'hash' not there
				if(r.group(11) == None):
					pass

				# 'hash' there...adding it
				else:
					self.data['hash'] = r.group(11)[1:]



			# who will handle error...me
			else:
				pass


	"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
	""""""							'update' the existing values or 'add' or 'delete' them					 """"""
	"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
	
	def update(self,key,value=None):
		uri_backup = self.uri
		Data = self.data
		
		result = update(key,value,Data)
		try:
			self.__init__(result)
			#print result
		except:
			self.uri = uri_backup
			self.data = Data
			raise Exception("syntax error in updating '%s' key"%(key))
				
				

