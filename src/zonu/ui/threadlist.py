#!/usr/bin/python

from PyQt4 import QtGui


class ThreadList(QtGui.QTreeWidget):
    """Displays a thread list.
    
    This class exposes an attribute 'thread_items', which maps
      (board_iden[model.BoardIden], thread_num[int]) -> _ThreadTreeWidgetItem
    """
    def __init__(self, parent, board_iden, config):
        QtGui.QTreeWidget.__init__(self, parent)
        self.board_iden = board_iden
        self.config = config
        self.setHeaderLabels(["Subject", "# Posts", "Author", "Thread #"]) 
        self.thread_items = {}
        
    def _Update(self, headlines):
        selected_items = self.selectedItems()  # Save selected items
        
        self.clear()
        self.thread_items = {}
        
        num_threads_to_list = self.config.general['num_threads_to_list']
        
        if len(headlines) > num_threads_to_list:
            headlines = headlines[:num_threads_to_list]
        
        for headline in headlines:
            item = _ThreadTreeWidgetItem(self, self.board_iden, headline.thread_num)
            item.setText(0, headline.subject)
            item.setText(1, str(headline.num_posts))
            item.setText(2, headline.author)
            item.setText(3, str(headline.thread_num)) 
            
            self.thread_items[(self.board_iden, headline.thread_num)] = item
            
        self.resizeColumnToContents(0)
        self.setColumnWidth(0, self.columnWidth(0) + 20)

        # Re-select previously selected items
        for item in selected_items:            
            new_item = [i for i in self.thread_items.values() if i == item][0]
            self.setItemSelected(new_item, True)
        
    def GetTreeWidget(self):
        return self


class _ThreadTreeWidgetItem(QtGui.QTreeWidgetItem):
    
    def __init__(self, parent, board_iden, thread_num):
        QtGui.QTreeWidgetItem.__init__(self, parent)
        self.board_iden = board_iden
        self.thread_num = thread_num
    
    def __eq__(self, other):
        return (self.board_iden == other.board_iden
                and self.thread_num == other.thread_num)
 