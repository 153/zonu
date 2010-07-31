#!/usr/bin/python

from PyQt4 import QtCore
from PyQt4 import QtWebKit


class ThreadView(QtWebKit.QWebView):
    
    def __init__(self, parent, config):
        QtWebKit.QWebView.__init__(self, parent)
        self.config = config
        self.thread_num = None
        self.thread_url = None
        
    def _update(self, thread_num, thread_url):
        self.thread_num = thread_num
        self.thread_url = thread_url
        self.get_web_view().load(QtCore.QUrl(thread_url))
        
    def get_web_view(self):
        return self
    
