#!/usr/bin/python


from PyQt4 import QtGui
import sidebar

class MainWindow(QtGui.QMainWindow):
    
    def __init__(self, config):
        QtGui.QMainWindow.__init__(self)
        
        self.config = config
        
        self.setWindowTitle('Zonu BBS Viewer')
        self.resize(config.main_window_size[0],
                    config.main_window_size[1])

        # Build the menu
        menu_bar = self.menuBar()
        bbs_menu = menu_bar.addMenu('&BBS')
        
        self.about_action = QtGui.QAction('About', self)
        self.about_action.setStatusTip('About Zonu')
        
        self.exit_action = QtGui.QAction('Exit', self)
        self.exit_action.setStatusTip('Exit Zonu')
        
        bbs_menu.addAction(self.about_action)
        bbs_menu.addAction(self.exit_action)
        
        # Put the sidebar and the right panel in an vsplitter        
        self.sidebar = sidebar.Sidebar(self, self.config)
        self.sidebar2 = sidebar.Sidebar(self, self.config)
        
        vsplitter = QtGui.QSplitter(self)
        
        vsplitter.addWidget(self.sidebar)
        vsplitter.addWidget(self.sidebar2)
        
        self.setCentralWidget(vsplitter)
        