#!/usr/bin/python

"""Unit tests for the zonu package."""

import unittest
import sys
from PyQt4 import QtCore
from PyQt4 import QtGui
import zonu
try:
    import mox
except ImportError:
    print 'Your need PyMox to run these unit tests. You can find it at:'
    print 'http://code.google.com/p/pymox/'
    sys.exit(0)


class ControllerTest(unittest.TestCase):

    def setUp(self):
        self.mocker = mox.Mox()
        self.app = self.mocker.CreateMock(QtGui.QApplication)
        self.view = self.mocker.CreateMock(zonu.ui.View)
        self.view.main_window = self.mocker.CreateMock(zonu.ui.MainWindow)
        self.view.main_window.about_action = self.mocker.CreateMock(QtGui.QAction)
        self.view.main_window.exit_action = self.mocker.CreateMock(QtGui.QAction)
        self.view.main_window.vsplitter = self.mocker.CreateMock(QtGui.QSplitter)
        self.view.main_window.sidebar = self.mocker.CreateMock(zonu.ui.Sidebar)
        self.view.main_window.sidebar.board_tree = self.mocker.CreateMock(zonu.ui.BoardTree)
        self.config = self.mocker.CreateMock(zonu.model.ConfigDir)
        self.config.boards_cache = self.mocker.CreateMock(zonu.model.BoardsCache)

    def test_initialize(self):
        # Create some site idens to use.
        site_idens = []        

        world4ch = zonu.model.SiteIden('world4ch', 'world4ch', 'World4ch',
                                       'http://dis.4chan.org', [])
        world4ch.board_idens.append(zonu.model.BoardIden(world4ch, 'prog', 'Programming', {}))        
        site_idens.append(world4ch)

        self.config.GetSiteIdens().AndReturn(site_idens)
        self.config.boards_cache.get_last_read(world4ch.board_idens[0]).AndReturn(None)
        
        self.mocker.ReplayAll()
        controller = zonu.controller.Controller(self.app, self.view, self.config)
        controller.initialize()
        self.mocker.VerifyAll()

    def test_bind_view(self):
        controller = zonu.controller.Controller(self.app, self.view, self.config)

        self.app.connect(self.app, QtCore.SIGNAL('lastWindowClosed()'),
                         controller._on_last_window_closed)

        mw = self.view.main_window
        mw.connect(mw.about_action, QtCore.SIGNAL('triggered()'),
                   controller._on_menu_about)
        
        mw.connect(mw.exit_action, QtCore.SIGNAL('triggered()'),
                   controller._on_menu_exit)
        
        mw.connect(mw.vsplitter, QtCore.SIGNAL('splitterMoved(int,int)'),
                   controller._on_main_window_vsplitter_moved)
        
        mw.connect(mw.sidebar.board_tree,
                   QtCore.SIGNAL('itemClicked(QTreeWidgetItem *, int)'),
                   controller._on_board_tree_click)
        mw.connect(mw.sidebar.board_tree,
                   QtCore.SIGNAL('updateSite(PyQt_PyObject)'),
                   controller._on_board_tree_update_site)
        mw.connect(mw.sidebar.board_tree,
                   QtCore.SIGNAL('markSiteAsRead(PyQt_PyObject)'),
                   controller._on_board_tree_mark_site_as_read)
                
        mw.connect(mw.sidebar.board_tree,
                   QtCore.SIGNAL('updateBoard(PyQt_PyObject)'),
                   controller._on_board_tree_update_board)
        
        mw.connect(mw.sidebar.board_tree,
                   QtCore.SIGNAL('markBoardAsRead(PyQt_PyObject)'),
                   controller._on_board_tree_mark_board_as_read)
        
        self.mocker.ReplayAll()
        controller.bind_view()
        self.mocker.VerifyAll()

if __name__ == '__main__':
    unittest.main()
                             
