# update.py for 'uri'
# to update 'uri' values
#
# leave 'value' argument, if want to delete a 'key'
# set a particular 'value' for a 'key' to add or update
#
# _author_ : Pravendra Singh <hackpravj@gmail.com>

import re

# options of keys that can be changed
options = ['scheme','host','port', 'path','query','hash','domain']

# supported protocols for 'scheme' value
protocols = ['http','https','view-source']

def querymaker(arg):
	length = len(arg)
	test = []
	token = True

	# local var for modified 'query' string
	queryStr = ''

	for i in range(0,length):
		if((re.match(r'^[a-zA-Z]+$',arg.keys()[i])) and (re.match(r'^[a-zA-Z0-9]+$',arg.values()[i]))):
			test.append(arg.keys()[i] + '=' + arg.values()[i])
		else:
			token = False
			raise Exception("syntax error in 'query' parameter %d"%(i+1))

	if(token):
		queryStr = '&'.join(test)

	return queryStr


# arguments are URI 'instance' itself and 'key'{whose 'value' is to be change} and 'value'{optional{leave if, want to delete}}
def update(key,value,Data):
	# 'key-value' pairs of already present data {a dictionary}
	Dict = Data
	# bool check
	Token = False
	# local var for modified 'query' string
	ans = ''
	# 'key' is valid
	if(key in options):

		# updating 'scheme/protocol'
		if(key == 'scheme'):
			# valid 'protocol'
			if(value in protocols):
				# update the 'scheme'
				Dict['scheme'] = value
				Token = True
			elif(value == None):
				# adding default 'protocol'
				Dict['scheme'] = 'http'
				Token = True
			# invalid 'protocol'
			else:
				raise Exception("un-supported protocol")

		# updating 'host'
		elif(key == 'host'):
			if(value == None):
				raise Exception("syntax error in 'host'")
			elif((value[:3] == 'www') and (re.match(r'^(\.[a-z0-9]+[a-z0-9\-]{0,1}[a-z0-9]{0,1}){2,}$',value[3:]))):
				Dict['host'] = value
				Token = True
			else:
				raise Exception("syntax error in 'host'")

		# updating 'port'
		elif(key == 'port'):
			if(value == None):
				Dict['port'] = value
				Token = True
			elif(re.match(r'[0-9]+',str(value))):
				Dict['port'] = value
				Token = True
			else:
				raise Exception("syntax error in 'port'")

		# updating 'path'
		elif(key == 'path'):
			if(value == None):
				Dict['path'] = ''
				Token = True
			elif(re.match(r'(\/[a-z0-9-_]+)+',value)):
				Dict['path'] = value
				Token = True
			else:
				raise Exception("syntax error in 'path'")

		# updating 'query'
		elif(key == 'query'):
			if(value == None):
				ans = ''
				Token = True
			elif(str(type(value)) == "<type 'dict'>"):
				if(len(Dict['query']) == 0):
					if(len(value) == 0):
						ans = ''
					else:
						ans = '?' + querymaker(value)
				else:
					if(len(value) == 0):
						ans = '?' + querymaker(Dict['query'])
					else:
						ans = '?' + querymaker(value)
				Token = True
			else:
				raise Exception("'query' parameter should be 'dict' type")

		# updating 'hash'
		elif(key == 'hash'):
			if(value == None):
				Dict['hash'] = ''
				Token = True
			elif(re.match(r'^[a-zA-Z0-9]+$',value)):
				Dict['hash'] = value
				Token = True
			else:
				raise Exception("syntax error in 'hash'")


		# making a new 'uri' from key-value pairs
		if(Token):
			result = Dict['scheme'] + '://' + Dict['host']

			if(Dict['port'] == None):
				pass
			else:
				result = result + ':' + str(Dict['port'])

			result = result + Dict['path']
		
			#result = result + ans
			if(key == 'query'):
				result = result + ans
			else:
				if(len(Dict['query']) == 0):
					ans = ''
					result = result + ans
				else:
					ans = '?' + querymaker(Dict['query'])
					result = result + ans

			if(Dict['hash'] == ''):
				pass
			else:
				result = result + '#' + Dict['hash']

			return result
		
	# 'key' is invalid
	else:
		raise Exception("the 'key' you entered for update, is invalid")
	