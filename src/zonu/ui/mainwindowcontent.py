#!/usr/bin/python


class MainWindowContent(object):    
    """Interface for content that can be displayed in the main window, next
    to the sidebar.
    
    Required Methods:
      get_main_widget() --> Return the main widget to be displayed
    
    Optional Methods:
      fix_sizes() --> Fix the sizes of your widget based on the config settings.
    """
    def __init__(self):
        assert hasattr(self, 'get_main_widget'), 'get_main_widget() method is required.'
    
    def fix_sizes(self):
        pass
    
