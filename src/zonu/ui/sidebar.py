#!/usr/bin/python

from PyQt4 import QtCore 
from PyQt4 import QtGui


class Sidebar(QtGui.QWidget):
    
    def __init__(self, parent, config):
        QtGui.QWidget.__init__(self, parent)
        self.config = config
        
        vbox = QtGui.QVBoxLayout()

        self.board_tree = _BoardTree(self, self.config) 
        vbox.addWidget(self.board_tree)        

        #self.watched_threads_btn = QtGui.QPushButton('Watched Threads', self)
        #vbox.addWidget(self.watched_threads_btn)
        
        self.setLayout(vbox)


class _BoardTree(QtGui.QTreeWidget):
    """A Board Tree that displays sites as items and their boards as their children.
    
    This widget supports a right-click menu. Connect to these signals to attach
    functionality:
    
    For sites in the board tree:
        updateSite(PyQt_PyObject)            # model.SiteIden
        markSiteAsRead(PyQt_PyQtObject)      # model.SiteIden
        
    For boards in the board tree:
        updateBoard(PyQt_PyObject)           # model.BoardIden 
        markBoardAsRead(PyQt_PyObject)       # model.BoardIden
    """
    def __init__(self, parent, config):
        QtGui.QTreeWidget.__init__(self, parent)        

        self.config = config
        
        # Set up the tree items
        self.setColumnCount(1)
        self.setHeaderLabel("All Boards")
        self.site_items = {}
        self.board_items = {}
        
        site_idens = self.config.GetSiteIdens()
        
        for site_iden in site_idens:
            site_item = _SiteTreeWidgetItem(self, site_iden)
            site_item.setText(0, site_iden.title)
            site_item.setExpanded(True)
            self.site_items[site_iden] = site_item
            
            for board_iden in site_iden.board_idens:
                board_item = _BoardTreeWidgetItem(site_item, board_iden)
                board_item.setText(0, board_iden.title)                
                self.board_items[board_iden] = board_item

    def contextMenuEvent(self, event):
        """Creates a custom right click menu for sites and boards."""
        
        item = self.itemAt(event.pos())
        
        if item in self.site_items.values():
            assert isinstance(item, _SiteTreeWidgetItem)            
            
            menu = QtGui.QMenu(self)
            
            update_all_action = menu.addAction('Update All Boards')
            menu.connect(update_all_action, QtCore.SIGNAL('triggered()'),
                         lambda: self.emit(QtCore.SIGNAL('updateSite(PyQt_PyObject)'),
                                                         item.site_iden))
            
            mark_all_as_read_action = menu.addAction('Mark All Boards as Read')
            menu.connect(mark_all_as_read_action, QtCore.SIGNAL('triggered()'),
                         lambda: self.emit(QtCore.SIGNAL('markSiteAsRead(PyQt_PyObject)'),
                                           item.site_iden))
            
            menu.exec_(event.globalPos())
        elif item in self.board_items.values():
            assert isinstance(item, _BoardTreeWidgetItem)
            menu = QtGui.QMenu(self)
            
            update_action = menu.addAction('Update')                        
            menu.connect(update_action, QtCore.SIGNAL('triggered()'),
                         lambda: self.emit(QtCore.SIGNAL('updateBoard(PyQt_PyObject)'),
                                           item.board_iden))
            
            mark_as_read_action = menu.addAction('Mark as Read')
            menu.connect(mark_as_read_action, QtCore.SIGNAL('triggered()'),
                         lambda: self.emit(QtCore.SIGNAL('markBoardAsRead(PyQt_PyObject)'),
                                           item.board_iden))
            
            menu.exec_(event.globalPos())

        
class _SiteTreeWidgetItem(QtGui.QTreeWidgetItem):
    
    def __init__(self, parent, site_iden):
        QtGui.QTreeWidgetItem.__init__(self, parent)
        self.site_iden = site_iden
        

class _BoardTreeWidgetItem(QtGui.QTreeWidgetItem):
    
    def __init__(self, parent, board_iden):
        QtGui.QTreeWidgetItem.__init__(self, parent)
        self.board_iden = board_iden
