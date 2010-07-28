#!/usr/bin/python

from PyQt4 import QtCore
from PyQt4 import QtGui
from zonu import model
import mainwindowcontent
import threadlist
import threadview


class BoardView(mainwindowcontent.MainWindowContent, QtGui.QSplitter):
    
    def __init__(self, parent, board_iden, config):
        mainwindowcontent.MainWindowContent.__init__(self)
        QtGui.QSplitter.__init__(self, parent)
        self.board_iden = board_iden
        self.config = config
        
        self.setOrientation(QtCore.Qt.Vertical)        
        
        self.thread_list = threadlist.ThreadList(self, board_iden, self.config)         
        self.thread_view = threadview.ThreadView(self, self.config)
    
        self.addWidget(self.thread_list)
        self.addWidget(self.thread_view)
            
    def GetMainWidget(self):
        return self
    
    def GetSplitter(self):
        return self
    
    def FixSizes(self):
        sizes = self.sizes()
        sizes[-1] = sizes[-1] + sizes[0] - self.config.ui['threadlist_height']
        sizes[0] = self.config.ui['threadlist_height']
        self.setSizes(sizes)
    
    def SetLoadingThread(self):
        pass 
    
    def UpdateHeadlines(self, headlines):
        self.thread_list._Update(headlines)
    
    def UpdateThreadURL(self, thread_num, thread_url):        
        self.thread_view._Update(thread_num, thread_url)
    