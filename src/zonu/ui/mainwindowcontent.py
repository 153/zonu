#!/usr/bin/python


class MainWindowContent(object):    
    
    def __init__(self):
        assert hasattr(self, 'GetMainWidget'), 'GetMainWidget() method is required.'
        