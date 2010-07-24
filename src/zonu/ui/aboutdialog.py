#!/usr/bin/python

import os
from PyQt4 import QtCore
from PyQt4 import QtGui


class AboutDialog(QtGui.QMainWindow):
    
    def __init__(self, parent):
        QtGui.QMainWindow.__init__(self, parent)
        
        self.setWindowTitle("About Zonu")
        self.resize(200, 200)
        
        screen = QtGui.QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move((screen.width()  - size.width())/2,
                  (screen.height() - size.height())/2)
        
        # Parent widget for the image and label
        widget = QtGui.QWidget(self)
        vbox = QtGui.QVBoxLayout()
        widget.setLayout(vbox)
        
        # The main logo
        image_path = os.path.join(os.path.abspath(os.path.dirname(__file__)),
                                  '..', 'data',  'zonu.png')
        image = QtGui.QLabel(widget)
        image.setPixmap(QtGui.QPixmap(image_path))
        image.setAlignment(QtCore.Qt.AlignCenter)
        vbox.addWidget(image)
        
        # The label
        label = QtGui.QLabel(widget)
        label.setAlignment(QtCore.Qt.AlignCenter)
        label.setText('Zonu, an Anonymous BBS Viewer')
        vbox.addWidget(label)
        
        # The link button
        self.button = QtGui.QPushButton(widget)
        self.button.setText("http://zonu.sageru.org")
        vbox.addWidget(self.button)
        
        self.setCentralWidget(widget)
        
