#!/usr/bin/python

from PyQt4 import QtCore
from PyQt4 import QtGui
import mainwindowcontent


class WelcomeScreen(mainwindowcontent.MainWindowContent, QtGui.QWidget):
    
    def __init__(self, parent):
        mainwindowcontent.MainWindowContent.__init__(self)
        QtGui.QWidget.__init__(self, parent)
        
        label = QtGui.QLabel('Welcome to Zonu')
        label.setAlignment(QtCore.Qt.AlignCenter)
        
        vbox = QtGui.QVBoxLayout(self)
        vbox.addWidget(label)
        
    def GetMainWidget(self):
        return self