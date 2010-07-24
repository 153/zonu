#!/usr/bin/python

from PyQt4 import QtCore
from zonu import model


class RetrieveHeadlinesThread(QtCore.QThread):
    """Use this thread to retrieve headlines in the background.
    
    When the headlines are retrieved, a 'ready(PyQt_PyObject)' signal is
    emitted, with the sole argument being an object with two attributes:
    'board_iden', which maps to the board iden, and 'headlines', which
    maps to a list of model.Headline instances.  
    """
    
    def __init__(self, board_iden):
        QtCore.QThread.__init__(self)        
        self.board_iden = board_iden
        
    def run(self):
        board = model.Board(self.board_iden)
        headlines = board.GetHeadlines()
        
        ret = _RetrieveHeadlinesReturn(self.board_iden, headlines)
        self.emit(QtCore.SIGNAL('ready(PyQt_PyObject)'), ret)


class _RetrieveHeadlinesReturn(object):
    
    def __init__(self, board_iden, headlines):
        self.board_iden = board_iden
        self.headlines = headlines
        