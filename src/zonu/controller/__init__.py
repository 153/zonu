#!/usr/bin/python

from PyQt4 import QtCore
from zonu import model
from zonu import ui
import retrieveboardthread


class Controller(object):
    
    def __init__(self, app, view, config):
        self.app = app
        self.view = view
        self.config = config
    
        self.thread_pool = []
    
    def BindView(self):
        # Connect with general app signals
        self.app.connect(self.app, QtCore.SIGNAL('lastWindowClosed()'),
                         self._OnLastWindowClosed)
        
        # Connect main window menu items
        mw = self.view.main_window
        
        mw.connect(mw.about_action, QtCore.SIGNAL('triggered()'),
                   self._OnMenuAbout)
        mw.connect(mw.exit_action, QtCore.SIGNAL('triggered()'),
                   self._OnMenuExit)
    
        # Connect to main window sidebar items
        mw.connect(mw.sidebar.board_tree,
                   QtCore.SIGNAL('itemClicked(QTreeWidgetItem *, int)'),
                   self._OnBoardTreeClick)
        
    def _OnLastWindowClosed(self):
        self._OnExit()

    def _OnMenuAbout(self):
        self.view.ShowAboutDialog()
    
    def _OnMenuExit(self):
        self._OnExit()
    
    def _OnBoardTreeClick(self, tree_widget_item, col):
        if isinstance(tree_widget_item, ui.sidebar._BoardTreeWidgetItem):
            loading_board_view = ui.LoadingBoardView(self.view.main_window)
            self.view.main_window.SetContent(loading_board_view)
            
            thread = retrieveboardthread.RetrieveBoardThread(tree_widget_item.board_iden)
            thread.connect(thread, QtCore.SIGNAL('ready(PyQt_PyObject)'),
                           self._OnBoardTreeClickBoardRetreivedReady)            
            thread.start()
            
            self.thread_pool.append(thread)

    def _OnBoardTreeClickBoardRetreivedReady(self, board):        
        board_view = ui.BoardView(self.view.main_window, self.config)
        board_view.UpdateHeadlines(board.GetHeadlines())
        self.view.main_window.SetContent(board_view)
    
    def _OnExit(self):
        self.config.main_window_size = (self.view.main_window.size().width(),
                                        self.view.main_window.size().height())
        
        self.config.Save()

        self.app.quit()
        