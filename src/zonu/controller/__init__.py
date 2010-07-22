#!/usr/bin/python

from PyQt4 import QtCore
from zonu import ui


class Controller(object):
    
    def __init__(self, app, view, config):
        self.app = app
        self.view = view
        self.config = config
    
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
    
    def _OnLastWindowClosed(self):
        self._OnExit()

    def _OnMenuAbout(self):
        self.view.ShowAboutDialog()
    
    def _OnMenuExit(self):
        self._OnExit()
    
    def _OnExit(self):
        self.config.main_window_size = (self.view.main_window.size().width(),
                                        self.view.main_window.size().height())
        
        self.config.Save()

        self.app.quit()
        