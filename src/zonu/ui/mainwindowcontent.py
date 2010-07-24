#!/usr/bin/python


class MainWindowContent(object):    
    """Interface for content that can be displayed in the main window, next
    to the sidebar.
    
    Required Methods:
      GetMainWidget() --> Return the main widget to be displayed
    
    Optional Methods:
      FixSizes() --> Fix the sizes of your widget based on the config settings.
    """
    def __init__(self):
        assert hasattr(self, 'GetMainWidget'), 'GetMainWidget() method is required.'
    
    def FixSizes(self):
        pass
    