#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# python library/script to interact with websms service
# on www.dhiraagu.com. part of the libDhiraagu (scoff!)
# project
#
# Copyright (C) 
#	2012 Naail Abdul Rahman (KudaNai)
#
# This is free software: you can redistribute it and/or modify 
# it under the terms of the GNU General Public License as published 
# by the Free Software Foundation, either version 3 of the License, 
# or (at your option) any later version.
#
# a copy of the license can be viewed at:
#      http://www.gnu.org/licenses/gpl.html
#
# This software is distributed in the hope that it will be useful, 
# but WITHOUT ANY WARRANTY; without even the implied warranty of 
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the 
# GNU General Public License for more details.
#


__author__  = "Naail Abdul Rahman"
__credits__ = ['you','me','all of the people','with nothing to do']
__version__ = "0.1"


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
	"""
	def __init__(self, username=None,password=None):
		self.username     = username
		self.password     = password
		self.sessionKey   = None
		self.messageCount = None

	
	def __str__(self):
		return "user: %s, session: %s, left:%s" % (self.username,self.sessionKey,self.messageCount)


	def set_user(self,username,password):
		"""
		set the username & password for the session user
		"""

		self.username   = username
		self.password   = password
		self.sessionKey = None
	

	def _OpenUrl(self,url,postdata=None,headers={}):
		"""
		helper method to open a url
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
		"""
		try:
			self.messageCount = int(re.search(r"send (\d+) more",response.read()).group(1))
		except:
			self.messageCount = None



	def authenticate(self):
		"""
		login to the server and get a sessionKey. 
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
