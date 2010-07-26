#!/usr/bin/python

import time
import urllib2
from PyQt4 import QtCore
from zonu import model


class RetrieveHeadlinesThread(QtCore.QThread):
    """Use this thread to retrieve headlines in the background.
    
    When the headlines are retrieved, a 'ready(PyQt_PyObject)' signal is
    emitted, with the sole argument being an object with two attributes:
    'board_iden' and 'board'.
    
    Optionally, this thread takes a "delay" parameter, which if specified,
    sets an amount of time (in seconds) to sleep before retrieving the
    headline.
    """
    def __init__(self, board_iden, delay=0):
        QtCore.QThread.__init__(self)        
        self.board_iden = board_iden
        self.delay = delay
        
    def run(self):
        time.sleep(self.delay)
        
        board = model.Board(self.board_iden)
        
        while True:
            try:
                board.GetHeadlines()
                break
            except urllib2.URLError:
                pass
        
        ret = _RetrieveHeadlinesResult(self.board_iden, board)
        self.emit(QtCore.SIGNAL('ready(PyQt_PyObject)'), ret)


class _RetrieveHeadlinesResult(object):
    
    def __init__(self, board_iden, board):
        self.board_iden = board_iden
        self.board = board
        