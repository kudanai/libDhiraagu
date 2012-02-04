# libDhiraagu

`libDhiraagu` is a collection of python libraries to interact with various web services provided by Dhiraagu (http://www.dhiraagu.com) - a local telco in Maldives.

it currently only contains the sms library

## components

### sms

currently the only library available,

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