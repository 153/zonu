#!/usr/bin/python

from PyQt4 import QtCore
from PyQt4 import QtGui
import mainwindowcontent

class LoadingBoardView(mainwindowcontent.MainWindowContent, QtGui.QLabel):
    def __init__(self, parent):
        mainwindowcontent.MainWindowContent.__init__(self)
        QtGui.QLabel.__init__(self, parent)
        
        self.setAlignment(QtCore.Qt.AlignCenter)
        self.setText('Loading board...')
    
    def get_main_widget(self):
        return self

