**libDhiraagu** is a collection of python libraries to interact with various web services provided by Dhiraagu (http://www.dhiraagu.com) - a local telco in Maldives.

## SMS

the project currently only provides one library i.e: for the webSMS service

**Usage**  

import the library: `from libDhiraagu.sms import WebSMS`

**create object**  

`mySpam = WebSMS('username','password')`.

alternatively you can use `mySpam = WebSMS()` followed by `mySpam.set_user('username','password')`.

**authenticating**  

`mySpam.authenticate()`  
will raise an exception on failure. Must authenticate at least once before trying to send messages, or after a session expires.

**sending messages**
  
`mySpam.send_sms('number','message')`  
will raise exceptions on invalid number, session expiry, or if you're not authenticated. returns true on success.


## standalone usage

additionally some components may be used directly from the command line. e.g. try: `python sms.py -h`