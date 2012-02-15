**libDhiraagu** is a collection of python libraries to interact with various web services provided by Dhiraagu (http://www.dhiraagu.com) - a local telco in Maldives.
## Documentation

**todo**

## demo apps

the sms.py library file has a cli interface and can be used directly from the command line. e.g. try: `python sms.py -h` for usage information.

trayApp.py is a simple pySide/qt4 application that will sit on the systemTray. click the icon to display a nice drop-down widget. (expect some problems with this behavior on windows). You will need to have Qt4 and pySide installed.(pyqt4 should work too - change `from pySide import…` to `from PyQt4 import…`)

![image](https://github.com/kudanai/libDhiraagu/raw/master/screenshots/trayApp.jpg)