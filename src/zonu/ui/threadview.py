#!/usr/bin/python

from PyQt4 import QtCore
from PyQt4 import QtWebKit


class ThreadView(QtWebKit.QWebView):
    
    def __init__(self, parent, config):
        QtWebKit.QWebView.__init__(self, parent)
        self.config = config
        
    def _Update(self, thread_url):
        self.GetWebView().load(QtCore.QUrl(thread_url))
        
    def GetWebView(self):
        return self