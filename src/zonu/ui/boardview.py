#!/usr/bin/python

from PyQt4 import QtGui
import mainwindowcontent
import threadlist

class BoardView(mainwindowcontent.MainWindowContent, QtGui.QSplitter):
    def __init__(self, parent, config):
        mainwindowcontent.MainWindowContent.__init__(self)
        QtGui.QSplitter.__init__(self, parent)
        
        self.config = config
        
        self.thread_list = threadlist.ThreadList(self, self.config)         
        self.addWidget(self.thread_list)
        
    def GetMainWidget(self):
        return self
        
    def UpdateHeadlines(self, headlines):
        self.thread_list._Update(headlines)
    
if __name__ == '__main__':
    BoardView()