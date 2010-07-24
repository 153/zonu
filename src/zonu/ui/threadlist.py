#!/usr/bin/python

from PyQt4 import QtGui


class ThreadList(QtGui.QTreeWidget):
    
    def __init__(self, parent, board_iden, config):
        QtGui.QTreeWidget.__init__(self, parent)
        self.board_iden = board_iden
        self.config = config
        self.setHeaderLabels(["Subject", "# Posts", "Author", "Thread #"]) 
        
    def _Update(self, headlines):
        self.clear()
        
        num_threads_to_list = self.config.general['num_threads_to_list']
        
        if len(headlines) > num_threads_to_list:
            headlines = headlines[:num_threads_to_list]
        
        for headline in headlines:
            item = _ThreadTreeWidgetItem(self, self.board_iden, headline.thread_num)
            item.setText(0, headline.subject)
            item.setText(1, str(headline.num_posts))
            item.setText(2, headline.author)
            item.setText(3, str(headline.thread_num))
            
    def GetTreeWidget(self):
        return self


class _ThreadTreeWidgetItem(QtGui.QTreeWidgetItem):
    
    def __init__(self, parent, board_iden, thread_num):
        QtGui.QTreeWidgetItem.__init__(self, parent)
        self.board_iden = board_iden
        self.thread_num = thread_num
    