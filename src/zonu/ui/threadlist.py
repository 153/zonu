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
        self.setHeaderLabels(["Subject", "# Posts"]) 
        self.thread_items = {}
        
    def _update_from_board(self, board):
        # Clear everything and re-add items.
        selected_items = self.selectedItems()  # save selected items
        
        self.clear()
        self.thread_items = {}
        
        headlines = board.headlines
        num_threads_to_list = self.config.num_threads_to_list
        
        if len(headlines) > num_threads_to_list:
            headlines = headlines[:num_threads_to_list]
        
        for headline in headlines:
            item = _ThreadTreeWidgetItem(self, self.board_iden, headline.thread_num)
            item.setText(0, headline.subject)
            item.setText(1, str(headline.num_posts))
            
            self.thread_items[(self.board_iden, headline.thread_num)] = item
            
        self.resizeColumnToContents(0)
        self.setColumnWidth(0, self.columnWidth(0) + 20)

        # Re-select previously selected items
        for item in selected_items:            
            new_item = [i for i in self.thread_items.values() if i == item]
            if new_item:
                self.setItemSelected(new_item[0], True)
        
        # Fix bolding of items
        for (board_iden, thread_num), item in self.thread_items.iteritems():
            last_read = self.config.boards_cache.get_last_read(board_iden)
            if thread_num in last_read.headlines:
                last_read_posts =  last_read.headlines[thread_num].num_posts
            else:
                last_read_posts = 0
                        
            last_retrieved = self.config.boards_cache.get_last_retrieved(board_iden)        
            if thread_num in last_retrieved.headlines:
                last_retrieved_posts = last_retrieved.headlines[thread_num].num_posts
            else:
                last_retrieved_posts = last_read_posts
            
            num_unread_posts = last_retrieved_posts - last_read_posts
            
            font = item.font(0)            
            if num_unread_posts > 0:
                font.setBold(True)
            else:
                font.setBold(False)                
            item.setFont(0, font)
            item.setFont(1, font)

    def get_tree_widget(self):
        return self


class _ThreadTreeWidgetItem(QtGui.QTreeWidgetItem):
    
    def __init__(self, parent, board_iden, thread_num):
        QtGui.QTreeWidgetItem.__init__(self, parent)
        self.board_iden = board_iden
        self.thread_num = thread_num
    
    def __eq__(self, other):
        return (self.board_iden == other.board_iden
                and self.thread_num == other.thread_num)
