#!/usr/bin/python2.5

from PyQt4 import QtCore
from zonu import model
from zonu import ui


class BoardUpdateThread(QtCore.QThread):
    
    def __init__(self, view, config, board_iden):
        QtCore.QThread.__init__(self, view.main_window)
        self.view = view
        self.config = config
        self.board_iden = board_iden
        
    def run(self):
        board = model.Board(self.board_iden)
            
        board_view = ui.BoardView(self.view.main_window, self.config)
        board_view.UpdateHeadlines(board.GetHeadlines())
            
        self.view.main_window.SetContent(board_view)
