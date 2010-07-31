#!/usr/bin/python

from PyQt4 import QtGui
from zonu.utils import logging
import sidebar
import welcomescreen


class MainWindow(QtGui.QMainWindow):
    
    def __init__(self, config):
        QtGui.QMainWindow.__init__(self)
        
        self.config = config
        
        self.setWindowTitle('Zonu BBS Viewer')
        self.resize(*config.main_window_size)
        
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
        self.vsplitter = QtGui.QSplitter(self)
        self.sidebar = sidebar.Sidebar(self, self.config)
        self.content = welcomescreen.WelcomeScreen(self).get_main_widget()
        
        self.vsplitter.addWidget(self.sidebar)
        self.vsplitter.addWidget(self.content)
        
        self.setCentralWidget(self.vsplitter)
    
    def resizeEvent(self, event):
        self.fix_sizes()
        self.content.fix_sizes()
    
    def set_content(self, content):
        self.content.get_main_widget().setVisible(False)
        self.vsplitter.addWidget(content)
        self.content = content

        content.fix_sizes()
        self.fix_sizes()
        
    def fix_sizes(self):
        sizes = self.vsplitter.sizes()
        sizes[-1] = sizes[-1] + sizes[0] - self.config.sidebar_width
        sizes[0] = self.config.sidebar_width
        self.vsplitter.setSizes(sizes)

    def update_board_tree(self, board_iden):
        """Updates a board tree in the board tree based on new results in the cache.

        This method takes a diff of the "last read" state and the "last retrieved"
        state and updates the label in the board tree according to this.
        """
        board_diff = self.config.boards_cache.gen_diff(board_iden)
        
        if board_diff.num_new_posts == 0:
            self.sidebar.board_tree.board_items[board_iden].setText(0, board_iden.title)
        elif board_diff.num_new_posts > 0:
            new_text = '%s (%d)' % (board_iden.title, board_diff.num_new_posts)
            self.sidebar.board_tree.board_items[board_iden].setText(0, new_text)
        else:
            logging.error('Board diff indicated a negative number of new posts for '
                          '(site, board) = (%s, %s). That number was %d.'
                          % (board_iden.site_iden.name, board_iden.name,
                             board_diff.num_new_posts))
