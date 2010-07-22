#!/usr/bin/python

from PyQt4 import QtGui
import mainwindowcontent

class LoadingBoardView(mainwindowcontent.MainWindowContent, QtGui.QLabel):
    def __init__(self, parent):
        mainwindowcontent.MainWindowContent.__init__(self)
        QtGui.QLabel.__init__(self, parent)
        
        self.setText('Loading board...')
    
    def GetMainWidget(self):
        return self

