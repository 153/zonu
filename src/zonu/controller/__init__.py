#!/usr/bin/python

import webbrowser
import os
from PyQt4 import QtCore
from zonu import model
from zonu import ui
import retrieveheadlinesthread
import retrievethreadthread


class Controller(object):
    
    def __init__(self, app, view, config):
        self.app = app
        self.view = view
        self.config = config
            
        self.thread_pool = []
    
        site_idens = self.config.GetSiteIdens()
        
        for site_iden in site_idens:
            for board_iden in site_iden.board_idens:
                if (board_iden in self.config.boards_cache['last_retrieved']
                    and board_iden in self.config.boards_cache['last_read']):
                    self._UpdateBoardTree(board_iden)
        
    def BindView(self):
        # Connect with general app signals
        self.app.connect(self.app, QtCore.SIGNAL('lastWindowClosed()'),
                         self._OnLastWindowClosed)
        
        # Connect main window menu items
        mw = self.view.main_window
        
        mw.connect(mw.about_action, QtCore.SIGNAL('triggered()'),
                   self._OnMenuAbout)
        mw.connect(mw.exit_action, QtCore.SIGNAL('triggered()'),
                   self._OnMenuExit)
    
        # Connect main window splitter
        mw.connect(mw.vsplitter, QtCore.SIGNAL('splitterMoved(int,int)'),
                   self._OnMainWindowVSplitterMoved)
        
        # Connect main window sidebar items
        mw.connect(mw.sidebar.board_tree,
                   QtCore.SIGNAL('itemClicked(QTreeWidgetItem *, int)'),
                   self._OnBoardTreeClick)
    
    
    def StartBackgroundTasks(self):
        """Overall procedure to start background tasks."""
        # Start tasks that look for thread updates every N minutes
        for site_iden in self.config.GetSiteIdens():
            for board_iden in site_iden.board_idens:
                self._StartBoardWatcherThread(board_iden)
    
    def _StartBoardWatcherThread(self, board_iden, delay=0):
        """Start a new board watcher thread. This is a thread that crawls a board
        for new updates and updates the item in the board tree with info from
        the board diff (for example a new post changes "SAoVQ" -> "SAoVQ (1)").
        """
        thread = retrieveheadlinesthread.RetrieveHeadlinesThread(board_iden, delay=delay)
        thread.connect(thread, QtCore.SIGNAL('ready(PyQt_PyObject)'),
                       self._OnBoardWatcherReady)
        thread.start()

        self.thread_pool.append(thread)
    
    def _OnBoardWatcherReady(self, result):
        """This method is called when a board watcher thread finished retrieving its results."""
        self.config.boards_cache['last_retrieved'][result.board_iden] = model.BoardState(result.board)
        
        if result.board_iden not in self.config.boards_cache['last_read']:
            self.config.boards_cache['last_read'][result.board_iden] = model.BoardState(result.board)
        
        self._UpdateBoardTree(result.board_iden)
        self._StartBoardWatcherThread(result.board_iden, delay=self.config.general['board_crawl_rate'])
    
    def _UpdateBoardTree(self, board_iden):
        """Update the board tree. This method takes a diff of the "last read" state
        and the "last retrieved" state and updates the label in the board tree according
        to this.
        """
        last_read_state = self.config.boards_cache['last_read'].get(board_iden)
        last_retrieved_state = self.config.boards_cache['last_retrieved'][board_iden]
        board_diff = last_retrieved_state.Diff(last_read_state)
        
        board_tree = self.view.main_window.sidebar.board_tree
        
        if board_diff.num_new_posts == 0:
            board_tree.board_items[board_iden].setText(0, board_iden.title)
        elif board_diff.num_new_posts > 0:
            new_text = '%s (%d)' % (board_iden.title, board_diff.num_new_posts)
            board_tree.board_items[board_iden].setText(0, new_text)
        
    def _OnLastWindowClosed(self):
        self._OnExit()

    def _OnMenuAbout(self):
        about_dialog = self.view.ShowAboutDialog()
        about_dialog.connect(about_dialog.button, QtCore.SIGNAL('clicked()'),
                             self._OnAboutDialogWebsiteButtonClick)
    
    def _OnMenuExit(self):
        self._OnExit()
    
    def _OnAboutDialogWebsiteButtonClick(self):
        webbrowser.open('http://zonu.sageru.org')
    
    def _OnMainWindowVSplitterMoved(self, pos, idx):
        self.config.ui['sidebar_width'] = pos
    
    def _OnBoardTreeClick(self, tree_widget_item, col):
        if isinstance(tree_widget_item, ui.sidebar._BoardTreeWidgetItem):
            # Here is what goes on here: If the board is in the cache, display the board
            # from the cache. If it's not, set a "Board loading..." screen. Either way,
            # dispatch a thread to query updates for the board and display them.                
            board_iden = tree_widget_item.board_iden
            
            if board_iden in self.config.boards_cache['boards']:
                board = self.config.boards_cache['boards'][board_iden]
                result = retrieveheadlinesthread._RetrieveHeadlinesResult(board_iden, board)
                self._OnBoardTreeClickBoardReady(result)
            else:
                loading_board_view = ui.LoadingBoardView(self.view.main_window)
                self.view.main_window.SetContent(loading_board_view)
            
            thread = retrieveheadlinesthread.RetrieveHeadlinesThread(board_iden)
            thread.connect(thread, QtCore.SIGNAL('ready(PyQt_PyObject)'),
                               self._OnBoardTreeClickBoardReady)            
            thread.start()
                
            self.thread_pool.append(thread)

    def _OnBoardTreeClickBoardReady(self, result):        
        self.config.boards_cache['last_retrieved'][result.board_iden] = model.BoardState(result.board)
        self.config.boards_cache['boards'][result.board_iden] = result.board
        
        board_view = ui.BoardView(self.view.main_window, result.board_iden,
                                  self.config)
        board_view.UpdateHeadlines(result.board.headlines)
        
        board_view.connect(board_view.GetSplitter(),
                           QtCore.SIGNAL('splitterMoved(int,int)'),
                           self._OnBoardViewSplitterMoved)

        board_view.connect(board_view.thread_list.GetTreeWidget(),
                           QtCore.SIGNAL('itemClicked(QTreeWidgetItem *, int)'),
                           self._OnThreadListItemClick)
        
        # Set threads in the thread list to be bold if they are newer than what
        # was last read.
        for (board_iden, thread_num), item in board_view.thread_list.thread_items.iteritems():
            if board_iden not in self.config.boards_cache['last_read']:
                continue
            
            last_retrieved_posts = self.config.boards_cache['last_retrieved'][board_iden].headlines[thread_num].num_posts
            if thread_num in self.config.boards_cache['last_read'][board_iden].headlines:
                last_read_posts =  self.config.boards_cache['last_read'][board_iden].headlines[thread_num].num_posts
            else:
                last_read_posts = 0
            
            num_unread_posts = last_retrieved_posts - last_read_posts
            
            if num_unread_posts > 0:
                font = item.font(0)
                font.setBold(True)
                item.setFont(0, font)
                item.setFont(1, font)
                item.setFont(2, font)
                item.setFont(3, font)   
        
        # Display the board view in the main window
        self.view.main_window.SetContent(board_view)
        
    def _OnBoardViewSplitterMoved(self, pos, idx):
        self.config.ui['threadlist_height'] = pos
        
    def _OnThreadListItemClick(self, tree_widget_item, col):
        self.view.main_window.content.SetLoadingThread()
        
        # Display this thread in the thread view 
        board_iden = tree_widget_item.board_iden
        thread_num = tree_widget_item.thread_num
        
        board = model.Board(board_iden)
        thread_url = board.GetThreadURL(thread_num, 'l40')
        
        self.view.main_window.content.UpdateThreadURL(thread_url)
        
        # Set the font in the thread list to not be bold, as we're reading this thread
        font = tree_widget_item.font(0)
        font.setBold(False)
        tree_widget_item.setFont(0, font)
        tree_widget_item.setFont(1, font)
        tree_widget_item.setFont(2, font)
        tree_widget_item.setFont(3, font)    
        
        # Update the (n) tag in the board tree
        self.config.boards_cache['last_read'][board_iden].headlines[thread_num] = \
            self.config.boards_cache['last_retrieved'][board_iden].headlines[thread_num]
        
        self._UpdateBoardTree(board_iden)
        
    def _OnThreadListItemClickReady(self, thread):
        self.view.main_window.content.UpdateThread(thread)
        
    def _OnExit(self):
        self.config.ui['sidebar_width'] = self.view.main_window.vsplitter.sizes()[0]
        
        self.config.ui['main_window_size'] = (self.view.main_window.size().width(),
                                              self.view.main_window.size().height())
        
        self.config.Save()

        self.app.quit()
        