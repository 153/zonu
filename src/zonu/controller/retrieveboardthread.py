#!/usr/bin/python2.5

from PyQt4 import QtCore
from zonu import model


class RetrieveBoardThread(QtCore.QThread):
    
    def __init__(self, board_iden):
        QtCore.QThread.__init__(self)        
        self.board_iden = board_iden
        
    def run(self):
        board = model.Board(self.board_iden)        
        self.emit(QtCore.SIGNAL('ready(PyQt_PyObject)'), board)
