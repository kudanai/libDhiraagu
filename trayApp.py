#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#
# Dhiraagu DeskSMS app
#
# Copyright (C) 
#	2012 Naail Abdul Rahman (KudaNai)
#
# This file is part of the libDhiraagu Project.
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


__author__  = "kudaNai (devel@kudanai.com)"
__version__ = "0.1a"
__license__ = "GPL"


from PySide 			import QtCore, QtGui
from libDhiraagu.sms 	import *



class Window(QtGui.QDialog):

        def __init__(self):
            super(Window, self).__init__()

            self.smsLib = WebSMS()  # does the window own this? gah!

            self.createWindowWidgets()

            self.createIcon()
            self.trayIcon.show()

            self.setWindowStyles()
            self.txtMessage.setFocus()
        
            self.trayIcon.activated.connect(self.messageClicked)
            self.txtUserName.textChanged.connect(self.resetUser)
            self.txtPassword.textChanged.connect(self.resetUser)



        def resetUser(self,text):
            # yes I know... i'm lazy so sue me
            self.smsLib.set_user(self.txtUserName.text(),self.txtPassword.text())


        def clearMessage(self):
            self.txtMessage.clear()
            self.txtMessage.setFocus()


        def sendClicked(self):

            if self.validateInputs():
                self.sendMessage()

        
        def validateInputs(self):
            if not self.txtUserName.text():
                self.txtUserName.setFocus()
                return False
            
            if not self.txtPassword.text():
                self.txtPassword.setFocus()
                return False
            
            if not self.validateNumber():
                self.txtNumber.setFocus()
                self.txtNumber.selectAll()
                return False

            return True

        
        def validateNumber(self):

            if self.txtNumber.text():
                try:
                    self.smsLib._validateNumber(self.txtNumber.text())
                except:
                    return False
                else:
                    return True
            else:
                return False


        def sendMessage(self):

            try:
                if not self.smsLib.sessionKey:
                    self.smsLib.authenticate()

                self.smsLib.send_sms(self.txtNumber.text(),self.txtMessage.toPlainText())

            except LoginError,e:
                self.trayIcon.showMessage("Error","could not log in",self.trayIcon.Warning)
                self.txtPassword.selectAll()
                self.txtPassword.setFocus()

            except Exception, e:
                #man .... check for the more specific stuff in an upcoming revision
                self.trayIcon.showMessage("Error",e,self.trayIcon.Critical)
                self.txtNumber.setFocus()

            else:
                self.trayIcon.showMessage("Success","you can send %s more messages" % self.smsLib.messageCount)
                print self.smsLib
                self.clearMessage()


        def createWindowWidgets(self):


            self.txtUserName = QtGui.QLineEdit()
            self.txtUserName.setPlaceholderText("username")
            self.txtUserName.setMaxLength(10)

            self.txtPassword = QtGui.QLineEdit()
            self.txtPassword.setPlaceholderText("password")
            self.txtPassword.setEchoMode(QtGui.QLineEdit.Password)
            self.txtPassword.setMaxLength(10)
            
            self.txtNumber = QtGui.QLineEdit()
            self.txtNumber.setInputMask('9999999')
            self.txtNumber.setPlaceholderText("7777777")
            self.lblNumber = QtGui.QLabel("Number",self.txtNumber)

            self.txtMessage = QtGui.QTextEdit()
            self.lblMessage = QtGui.QLabel("Message",self.txtMessage)

            self.btnClear = QtGui.QPushButton("&Clear", self)
            self.btnClear.clicked.connect(self.clearMessage)

            self.btnSend = QtGui.QPushButton("&Send", self)
            self.btnSend.clicked.connect(self.sendClicked)


            self.setWidgetLayout()


        def setWidgetLayout(self):

            loginLayout = QtGui.QHBoxLayout()
            loginLayout.addWidget(self.txtUserName)
            loginLayout.addWidget(self.txtPassword)

            buttonLayout = QtGui.QHBoxLayout()
            buttonLayout.addWidget(self.btnClear)
            buttonLayout.addWidget(self.btnSend)

            mainLayout = QtGui.QVBoxLayout()
            mainLayout.addLayout(loginLayout)
            mainLayout.addWidget(self.lblNumber)
            mainLayout.addWidget(self.txtNumber)
            mainLayout.addWidget(self.lblMessage)
            mainLayout.addWidget(self.txtMessage)
            mainLayout.addLayout(buttonLayout)

            self.setLayout(mainLayout)


        def setWindowStyles(self):

            self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint | QtCore.Qt.FramelessWindowHint)
            self.setWindowOpacity(0.95)

            self.setStyleSheet("""
                QDialog{
                    background : #303030;
                    max-height : 300px;
                    max-width  : 250px;
                }

                QLabel{
                    color:#808080;
                    margin-top: 2px;
                }

                QLineEdit,QTextEdit{
                    background: #404040;
                    padding:2px;
                    border:1px solid #484848;
                    color:#FF3366;
                }
                QTextEdit{
                    border-radius:10px;
                }
                QPushButton{
                    border-radius : 5px;
                    background: #444444;
                    min-height:25px;
                    margin:3px;
                    color: #BBBBBB;
                }
                QPushButton:hover{
                     /* color:#EE2200; */
                    background: #555555
                }
                QPushButton:pressed{
                     /* color:#EEEE00; */
                    background: #666666
                }
            """)


        def repositionWindow(self):
            x1,y1 = self.trayIcon.geometry().center().toTuple()
            windowWidth = self.geometry().width()
             
            self.move(x1 - windowWidth//2,y1*2 + 5)
            pass

            # TODO: write code here to reposition the window close
            # to the systray icon


        def messageClicked(self,trigger):

            if self.isVisible():
                self.hide()
            else:
                self.repositionWindow()
                self.show()
                self.setFocus()


        def createIcon(self):

            icon = QtGui.QIcon("res/icon.png")

            self.trayIcon = QtGui.QSystemTrayIcon(self)

            self.trayIcon.setIcon(icon)
                        
            # TODO: check right click only activation
            # self.trayIconMenu = QtGui.QMenu(self)
            # self.trayIconMenu.addAction(QtGui.QAction("&Quit", self,triggered=QtGui.qApp.quit))
            # self.trayIcon.setContextMenu(self.trayIconMenu)



if __name__ == '__main__':

    import sys

    app = QtGui.QApplication(sys.argv)

    icon = QtGui.QIcon("res/icon.png")
    app.setWindowIcon(icon)


    if not QtGui.QSystemTrayIcon.isSystemTrayAvailable() or not QtGui.QSystemTrayIcon.supportsMessages():

        QtGui.QMessageBox.critical(None, "Systray",	
                "Could not create systray icon and messaging protocol. Going to quit now")
               
        sys.exit(1)

    QtGui.QApplication.setQuitOnLastWindowClosed(False)

    window = Window()

    sys.exit(app.exec_())