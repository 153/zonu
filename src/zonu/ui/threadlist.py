#!/usr/bin/python

from PyQt4 import QtGui


class ThreadList(QtGui.QListView):
    
    def __init__(self, parent):
        QtGui.QListView.__init__(self, parent)
        
    