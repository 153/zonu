#!/usr/bin/python

from PyQt4 import QtGui


class ThreadList(QtGui.QTreeWidget):
    
    def __init__(self, parent, config):
        QtGui.QTreeWidget.__init__(self, parent)
        self.config = config
        self.setHeaderLabels(["Subject", "# Posts", "Author", "Thread #"]) 
        
    def _Update(self, headlines):
        self.clear()
        
        if len(headlines) > self.config.num_threads_to_list:
            headlines = headlines[:self.config.num_threads_to_list]
        
        for headline in headlines:
            item = QtGui.QTreeWidgetItem(self)
            item.setText(0, headline.subject)
            item.setText(1, str(headline.num_posts))
            item.setText(2, headline.author)
            item.setText(3, str(headline.thread_num))