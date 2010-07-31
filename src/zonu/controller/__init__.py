#!/usr/bin/python

import os
import time
import urlparse
import webbrowser
from PyQt4 import QtCore
from PyQt4 import QtWebKit
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
        
        mw.connect(mw.sidebar.board_tree,
                   QtCore.SIGNAL('updateSite(PyQt_PyObject)'),
                   self._OnBoardTreeUpdateSite)
        mw.connect(mw.sidebar.board_tree,
                   QtCore.SIGNAL('markSiteAsRead(PyQt_PyObject)'),
                   self._OnBoardTreeMarkSiteAsRead)
        
        
        mw.connect(mw.sidebar.board_tree,
                   QtCore.SIGNAL('updateBoard(PyQt_PyObject)'),
                   self._OnBoardTreeUpdateBoard)
        
        mw.connect(mw.sidebar.board_tree,
                   QtCore.SIGNAL('markBoardAsRead(PyQt_PyObject)'),
                   self._OnBoardTreeMarkBoardAsRead)
        
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
        """This method is called when a board watcher thread finished
        retrieving its results."""
        self.config.boards_cache['last_retrieved'][result.board_iden] = model.BoardState(result.board)
        self.config.boards_cache['boards'][result.board_iden] = result.board
        
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
        board_items = self.view.main_window.sidebar.board_tree.board_items.values()
        
        if tree_widget_item in board_items:
            # Here what goes on here: If the board is in the cache, display the board from
            # the cache, then dispatch a thread to look for updates. If it's not, set a
            # "Board loading..." screen and dispatch a thread to query the headlines for the
            # board and display them.                
            board_iden = tree_widget_item.board_iden
            
            if board_iden in self.config.boards_cache['boards']:
                board = self.config.boards_cache['boards'][board_iden]
                result = retrieveheadlinesthread._RetrieveHeadlinesResult(board_iden, board)
                self._OnBoardTreeClickBoardReady(result)
                
                thread = retrieveheadlinesthread.RetrieveHeadlinesThread(board_iden)
                thread.connect(thread, QtCore.SIGNAL('ready(PyQt_PyObject)'),
                               self._OnBoardViewNewHeadlinesReady)
                thread.start()
                
                self.thread_pool.append(thread)
            else:
                loading_board_view = ui.LoadingBoardView(self.view.main_window)
                self.view.main_window.SetContent(loading_board_view)
            
                thread = retrieveheadlinesthread.RetrieveHeadlinesThread(board_iden)
                thread.connect(thread, QtCore.SIGNAL('ready(PyQt_PyObject)'),
                               self._OnBoardTreeClickBoardReady)            
                thread.start()
                
                self.thread_pool.append(thread)
                
    
    def _BoldThreadListItems(self, thread_list):
        """Set threads in the thread list to be bold if they are newer than what
        was last read.
        """
        assert isinstance(thread_list, ui.ThreadList)
        
        for (board_iden, thread_num), item in thread_list.thread_items.iteritems():
            if board_iden not in self.config.boards_cache['last_read']:
                continue
            
            if thread_num in self.config.boards_cache['last_read'][board_iden].headlines:
                last_read_posts =  self.config.boards_cache['last_read'][board_iden].headlines[thread_num].num_posts
            else:
                last_read_posts = 0
            
            if thread_num in self.config.boards_cache['last_retrieved'][board_iden].headlines:
                last_retrieved_posts = self.config.boards_cache['last_retrieved'][board_iden].headlines[thread_num].num_posts
            else:
                last_retrieved_posts = last_read_posts
            
            num_unread_posts = last_retrieved_posts - last_read_posts
            
            font = item.font(0)
            
            if num_unread_posts > 0:
                font.setBold(True)
            else:
                font.setBold(False)
                
            item.setFont(0, font)
            item.setFont(1, font)
            item.setFont(2, font)
            item.setFont(3, font)
            
    def _OnBoardViewNewHeadlinesReady(self, result):
        
        if result.board_iden in self.config.boards_cache['last_retrieved']:
            last_retrieved = self.config.boards_cache['last_retrieved'][result.board_iden]
            last_retrieved = last_retrieved.Union(model.BoardState(result.board))
            self.config.boards_cache['last_retrieved'][result.board_iden] = last_retrieved
        else: 
            self.config.boards_cache['last_retrieved'][result.board_iden] = model.BoardState(result.board)
                    
        self.config.boards_cache['boards'][result.board_iden] = result.board
        
        if isinstance(self.view.main_window.content, ui.BoardView):
            board_view = self.view.main_window.content
        
            if result.board_iden == board_view.board_iden:    
                board_view.UpdateHeadlines(result.board.headlines)
                self._BoldThreadListItems(board_view.thread_list)
        
        self._UpdateBoardTree(result.board_iden)
        
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
        
        # Display the board view in the main window
        self.view.main_window.SetContent(board_view)
        self._BoldThreadListItems(board_view.thread_list)
    
    def _OnBoardTreeUpdateSite(self, site_iden):
        """When the user specifies to update all boards in a site via the
        right click menu."""
        for board_iden in site_iden.board_idens:
            self._OnBoardTreeUpdateBoard(board_iden)
        
    def _OnBoardTreeMarkSiteAsRead(self, site_iden):
        """When the user specifies to mark all boards in a site as read via
        the right-click menu."""
        for board_iden in site_iden.board_idens:
            self._OnBoardTreeMarkBoardAsRead(board_iden)

    def _OnBoardTreeUpdateBoard(self, board_iden):
        """When the user specifies to force an update of a board."""
        # Note: this callback method will only update the GUI if the board
        # is being displayed, so it is safe to call here where this may not
        # be the case.
        thread = retrieveheadlinesthread.RetrieveHeadlinesThread(board_iden)
        thread.connect(thread, QtCore.SIGNAL('ready(PyQt_PyObject)'),
                       self._OnBoardViewNewHeadlinesReady)
        thread.start()

        self.thread_pool.append(thread)                

    def _OnBoardTreeMarkBoardAsRead(self, board_iden):
        """When the user specifies to mark board as read via the right click menu."""
        last_read = self.config.boards_cache['last_read'][board_iden]
        last_retrieved = self.config.boards_cache['last_retrieved'][board_iden]
        
        last_read = last_read.Union(last_retrieved)
        
        self.config.boards_cache['last_read'][board_iden] = last_read
        
        self._UpdateBoardTree(board_iden)
        
        if isinstance(self.view.main_window.content, ui.BoardView):
            thread_list = self.view.main_window.content.thread_list
            
            if board_iden == thread_list.board_iden:                
                self._BoldThreadListItems(thread_list)
            
        
    def _OnBoardViewSplitterMoved(self, pos, idx):
        self.config.ui['threadlist_height'] = pos
        
    def _OnThreadListItemClick(self, tree_widget_item, col):
        self.view.main_window.content.SetLoadingThread()
        
        # Display this thread in the thread view 
        board_iden = tree_widget_item.board_iden
        thread_num = tree_widget_item.thread_num
        
        board = model.Board(board_iden)
        thread_url = board.GetThreadURL(thread_num, 'l40')
        
        self.view.main_window.content.UpdateThreadURL(thread_num, thread_url)
        
        # Connect with the link clicked signal in the thread web view
        thread_view = self.view.main_window.content.thread_view
        
        thread_view.page().setLinkDelegationPolicy(QtWebKit.QWebPage.DelegateExternalLinks)
        thread_view.connect(thread_view.GetWebView(),
                            QtCore.SIGNAL('linkClicked(const QUrl&)'),
                            self._OnThreadViewLinkClicked)
        
        thread_view.connect(thread_view.GetWebView(),
                            QtCore.SIGNAL('urlChanged(QUrl)'),
                            self._OnThreadViewURLChanged)
        
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
    
    def _OnThreadViewLinkClicked(self, qurl, links_opened={}):
        """Triggered when the user clicks a link inside a thread view."""
        url = str(qurl.toString())
        
        # First, we block attempts to reach the board page to prevent leaving
        # the sandbox.
        board = model.Board(self.view.main_window.content.board_iden)
        if url in board.GetBoardURLs():
            return
        
        # Open new links in a new window if they are from a different server. Ie,
        # if the thread is on dis.4chan.org, anything that's not on dis.4chan.org
        # will be opened in a new window.        
        thread_url = self.view.main_window.content.thread_view.thread_url
        
        url_netloc = urlparse.urlparse(url).netloc
        thread_netloc = urlparse.urlparse(thread_url).netloc
                
        if url_netloc == thread_netloc:
            board_view = self.view.main_window.content 
            thread_num = board_view.thread_view.thread_num
            board_view.UpdateThreadURL(thread_num, url)
        else:
            # There is a nasty bug in Qt webkit that is for some reason triggering
            # linkClicked(QUrl&) multiple times for a single click. To work around
            # this we prevent opening the link more than once in 50ms.
            if url in links_opened and time.time() - links_opened[url] < .05:                
                pass  # Block opening link
            else:
                links_opened[url] = time.time()
                webbrowser.open(url)
    
    def _OnThreadViewURLChanged(self, qurl):
        """Triggered when the URL changes."""
        # What we do here is intercept loads of the board URL, assuming they
        # are redirects after the user has posted. Instead, we send the user
        # back to the thread they just posted in.
        board_view = self.view.main_window.content 
        thread_view = board_view.thread_view
        url =  str(qurl.toString())
        
        board = model.Board(board_view.board_iden)        
        
        if url in board.GetBoardURLs():
            thread_num = thread_view.thread_num    
            target_url = board.GetThreadURL(thread_num, 'l5')        
            board_view.UpdateThreadURL(thread_num, target_url)
            
            # Update last read cache so we don't think our own post is new
            last_read_state = self.config.boards_cache['last_read'][board_view.board_iden] 
            last_read_state.headlines[thread_num].num_posts += 1
            
    def _OnExit(self):
        self.config.ui['sidebar_width'] = self.view.main_window.vsplitter.sizes()[0]
        
        self.config.ui['main_window_size'] = (self.view.main_window.size().width(),
                                              self.view.main_window.size().height())
        
        self.config.Save()

        self.app.quit()
        