#!/usr/bin/python

from PyQt4 import QtGui


class AboutDialog(QtGui.QDialog):
    
    def __init__(self, parent):
        QtGui.QDialog.__init__(self, parent=parent)
        
        self.setWindowTitle("About Zonu")
        self.resize(200, 200)
        
        screen = QtGui.QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move((screen.width()  - size.width())/2,
                  (screen.height() - size.height())/2)