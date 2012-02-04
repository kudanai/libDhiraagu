#!/usr/bin/env python

import urllib
import urllib2
import re


class InvalidNumberFormat(Exception):
	pass

class LoginError(Exception):
	pass

class SessionExpired(Exception):
	pass

class QuotaExceeded(Exception):
	pass

class NotAuthenticated(Exception):
	pass


class WebSMS():
	"""
	WebSMS class to send SMS's through Dhiraagu's webSMS portal
	on http://www.dhiraagu.com
	
	@param username the username for the instance (string)
	@param password the password for the instance (string)
	"""
	def __init__(self, username=None,password=None):
		self.username     = username
		self.password     = password
		self.sessionKey   = None
		self.messageCount = None



	def set_user(self,username,password):
		"""
			set the username & password for the session user

			@param username the username for the instance (string)
			@param password the password for the instance (string)
		"""

		self.username   = username
		self.password   = password
		self.sessionKey = None
	


	def _OpenUrl(self,url,postdata=None,headers={}):
		"""
			helper method to open a url

			@param url the url to post to (string)
			@param postdata the post data (dictionary)
			@param headers url-headers (dictionary)
		"""

		value   = urllib.urlencode(postdata)
		request = urllib2.Request(url,value,headers)

		# if something comes up, it's up to the  owner to handle the exception
		try:
			response = urllib2.urlopen(request)
		except:
			raise
		else:
			return response



	def _validateNumber(self,number):
		"""
			helper method to validate cell number 

			@param number the number to validate (string)
			@returns (boolean)
		"""
		try:
			match = re.match(r"^7[6-9][0-9]{5}$",number)
		except:
			raise InvalidNumberFormat,"number must be passed as string"
		else:
			if match:
				return True
			else:
				raise InvalidNumberFormat,"incorrect number format"



	def _parseMessageCount(self,response):
		"""
			accepts a responseObject. Looks for the remaining
			number of messages a user is allowed to send. If this
			is absent, the session probably expired

			sets instance variable

			@param response HTTPResonseObject
		"""
		try:
			self.messageCount = int(re.search(r"send (\d+) more",response.read()).group(1))
		except:
			self.messageCount = None



	def authenticate(self):
		"""
			login to the server and get a sessionKey. 
			@returns (boolean)
		"""

		if not self.username or not self.password: return False

		response = self._OpenUrl("http://websms.dhimobile.com.mv/cgi-bin/websms/index.pl",
									{ 'username': self.username,
									  'password': self.password
									}
								)

		if response.headers.has_key('set-cookie'):
			cookiestring = response.headers['set-cookie']
			try:
				# ugly references here beware
				self.sessionKey   = re.match(r"Dhi=(\d+);",cookiestring).group(1)
				self._parseMessageCount(response)
				return True
			except:
				self.sessionKey   = None
				self.messageCount = None
				raise LoginError,"no session key returned by server"
		else:
			raise LoginError,"no session key returned by server"	#again? tsk!!!


	def send_sms(self,number,message):
		"""
			send the message to specified number.
			message will be truncated at 140 chars.
			TODO: raise an exception if that happens

			@param number the number to send message to (string) !important
			@message the message to send (string)
			@return boolean
		"""
 		if not self.sessionKey: 
	 		raise NotAuthenticated,"must be authenticated first"

		self._validateNumber(number)

		myMessage = message[:140]

		response = self._OpenUrl("http://websms.dhimobile.com.mv/cgi-bin/websms/send_message.pl",
									{'mobilenumber': number,'message': myMessage},
									{'Cookie': 'Dhi=%s' % self.sessionKey}
								)

		self._parseMessageCount(response)

		if not self.messageCount:
			self.sessionKey = None
			raise SessionExpired,"Session expired..probably"



if __name__ == '__main__':

	import argparse
	import getpass

	parser = argparse.ArgumentParser( description="Send SMS's to dhiraagu subscribers through their websms portal",
									  epilog="2010 - KudaNai (http://kudanai.com)\nand that's how a cookie crumbles")

	parser.add_argument('-n','--number',required=True,metavar='NUMBER',help="specify the phone number",type=str)
	parser.add_argument('-u','--user',required=True,metavar='USERNAME',help="the username to use (password will be prompted)",type=str)
	parser.add_argument('-m','--message',required=True,metavar='MESSAGE',help="The message to send. watch out for escapes",type=str)

	args  	   = parser.parse_args()
	args.passw = getpass.getpass()

	mySMS = WebSMS(args.user,args.passw)

	try:
		print "logging in..."
		mySMS.authenticate()
		mySMS.send_sms(args.number,args.message)
		print "message sent!"
		print "messages remaining = %d" % mySMS.messageCount
	except InvalidNumberFormat,e:
		print "Error",e
	except LoginError,e:
		print "correct user?",e
	except Exception,e:
		print e
