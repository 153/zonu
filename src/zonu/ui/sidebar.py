
from PyQt4 import QtGui


class Sidebar(QtGui.QWidget):
    
    def __init__(self, parent, config):
        QtGui.QWidget.__init__(self, parent)
        self.config = config
        
        vbox = QtGui.QVBoxLayout()

        self.board_tree = _BoardTree(self, self.config) 
        vbox.addWidget(self.board_tree)        

        self.watched_threads_btn = QtGui.QPushButton('Watched Threads', self)
        vbox.addWidget(self.watched_threads_btn)
        
        self.setLayout(vbox)


class _BoardTree(QtGui.QTreeWidget):
        
    def __init__(self, parent, config):
        QtGui.QTreeWidget.__init__(self, parent)        

        self.config = config
        self.setColumnCount(1)
        self.setHeaderLabel("All Boards")
        self.site_items = {}
        self.board_items = {}
        
        site_idens = self.config.GetSiteIdens()
        
        for site_iden in site_idens:
            site_item = QtGui.QTreeWidgetItem(self)
            site_item.setText(0, site_iden.title)
            site_item.setExpanded(True)
            self.site_items[site_iden] = site_item
            
            for board_iden in site_iden.board_idens:
                board_item = _BoardTreeWidgetItem(site_item, board_iden)
                board_item.setText(0, board_iden.title)                
                self.board_items[board_iden] = board_item

class _BoardTreeWidgetItem(QtGui.QTreeWidgetItem):
    
    def __init__(self, parent, board_iden):
        QtGui.QTreeWidgetItem.__init__(self, parent)
        self.board_iden = board_iden
        