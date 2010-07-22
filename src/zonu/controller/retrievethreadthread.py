#!/usr/bin/python

from PyQt4 import QtCore
from zonu import model


class RetrieveThreadThread(QtCore.QThread):
    """Use this thread to retrieve a thread in the background.
    
    When the board is retrieved, a 'ready(PyQt_PyObject)' signal is
    emitted, with the sole argument being the model.Thread instance.    
    """
    
    def __init__(self, board_iden, thread_num):
        QtCore.QThread.__init__(self)        
        self.board_iden = board_iden
        self.thread_num = thread_num
        
    def run(self):
        board = model.Board(self.board_iden)
        thread = board.GetThread(self.thread_num)        
        self.emit(QtCore.SIGNAL('ready(PyQt_PyObject)'), thread)
