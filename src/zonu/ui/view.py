#!/usr/bin/python

import mainwindow
import aboutdialog


class View(object):
    def __init__(self, config):
        self.config = config
        
        self.main_window = mainwindow.MainWindow(config)
        self.main_window.show()
        self.main_window.fix_sizes()
    
    def ShowAboutDialog(self):
        about_dialog = aboutdialog.AboutDialog(self.main_window)
        about_dialog.show() 
        return about_dialog
    
