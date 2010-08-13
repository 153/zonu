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
    
    def initialize(self):
        """Initialize the controller. This should be called immediately after
        instantiation."""
        site_idens = self.config.GetSiteIdens()
        
        for site_iden in site_idens:
            for board_iden in site_iden.board_idens:
                if (self.config.boards_cache.get_last_read(board_iden) is not None
                    and self.config.boards_cache.get_last_retrieved(board_iden) is not None):
                    
                    self.view.main_window.update_board_tree(board_iden)
        
    def bind_view(self):
        # Connect with general app signals
        self.app.connect(self.app, QtCore.SIGNAL('lastWindowClosed()'),
                         self._on_last_window_closed)
        
        # Connect main window menu items
        mw = self.view.main_window
        
        mw.connect(mw.about_action, QtCore.SIGNAL('triggered()'),
                   self._on_menu_about)
        mw.connect(mw.exit_action, QtCore.SIGNAL('triggered()'),
                   self._on_menu_exit)
        
        # Connect main window splitter
        mw.connect(mw.vsplitter, QtCore.SIGNAL('splitterMoved(int,int)'),
                   self._on_main_window_vsplitter_moved)
        
        # Connect main window sidebar items
        mw.connect(mw.sidebar.board_tree,
                   QtCore.SIGNAL('itemClicked(QTreeWidgetItem *, int)'),
                   self._on_board_tree_click)
        
        mw.connect(mw.sidebar.board_tree,
                   QtCore.SIGNAL('updateSite(PyQt_PyObject)'),
                   self._on_board_tree_update_site)
        mw.connect(mw.sidebar.board_tree,
                   QtCore.SIGNAL('markSiteAsRead(PyQt_PyObject)'),
                   self._on_board_tree_mark_site_as_read)
        
        
        mw.connect(mw.sidebar.board_tree,
                   QtCore.SIGNAL('updateBoard(PyQt_PyObject)'),
                   self._on_board_tree_update_board)
        
        mw.connect(mw.sidebar.board_tree,
                   QtCore.SIGNAL('markBoardAsRead(PyQt_PyObject)'),
                   self._on_board_tree_mark_board_as_read)
        
    def start_bg_tasks(self):
        """Overall procedure to start background tasks."""
        # Start tasks that look for thread updates every N minutes
        for site_iden in self.config.GetSiteIdens():
            for board_iden in site_iden.board_idens:
                self._start_board_watcher_thread(board_iden)
    
    def _start_board_watcher_thread(self, board_iden, delay=0):
        """Start a new board watcher thread. This is a thread that crawls a board
        for new updates and updates the item in the board tree with info from
        the board diff (for example a new post changes "SAoVQ" -> "SAoVQ (1)").
        """
        thread = retrieveheadlinesthread.RetrieveHeadlinesThread(board_iden, delay=delay)
        thread.connect(thread, QtCore.SIGNAL('ready(PyQt_PyObject)'),
                       self._on_board_watcher_thread_ready)
        thread.start()

        self.thread_pool.append(thread)
    
    def _on_board_watcher_thread_ready(self, result):
        """This method is called when a board watcher thread finished
        retrieving its results."""
        self.config.boards_cache.update_last_retrieved(result.board)
        
        #if result.board_iden not in self.config.boards_cache['last_read']:
        #    self.config.boards_cache['last_read'][result.board_iden] = model.BoardState(result.board)
        
        self.view.main_window.update_board_tree(result.board_iden)     
        self._start_board_watcher_thread(result.board_iden, delay=self.config.board_crawl_rate)
        
    def _on_last_window_closed(self):
        """Called when the last window is closed."""
        self._on_exit()

    def _on_menu_about(self):
        """When 'About Zonu' is selected from the menu."""
        about_dialog = self.view.ShowAboutDialog()
        about_dialog.connect(about_dialog.button, QtCore.SIGNAL('clicked()'),
                             self._on_about_dialog_website_button_click)
    
    def _on_menu_exit(self):
        """When 'Exit' is selected from the menu."""
        self._on_exit()
    
    def _on_about_dialog_website_button_click(self):
        """When the user clicks the website button in the about dialog."""
        webbrowser.open('http://zonu.sageru.org')
    
    def _on_main_window_vsplitter_moved(self, pos, idx):
        self.config.sidebar_width = pos
    
    def _on_board_tree_click(self, tree_widget_item, col):
        board_items = self.view.main_window.sidebar.board_tree.board_items.values()
        
        if tree_widget_item in board_items:
            # Here what goes on here: If the board is in the cache, display the board from
            # the cache, then dispatch a thread to look for updates. If it's not, set a
            # "Board loading..." screen and dispatch a thread to query the headlines for the
            # board and display them.                
            board_iden = tree_widget_item.board_iden
            
            if self.config.boards_cache.get_last_retrieved(board_iden) is not None:
                board = self.config.boards_cache.get_last_retrieved(board_iden).to_board()
                result = retrieveheadlinesthread._RetrieveHeadlinesResult(board_iden, board)
                self._on_board_view_click_board_ready(result)
                
                thread = retrieveheadlinesthread.RetrieveHeadlinesThread(board_iden)
                thread.connect(thread, QtCore.SIGNAL('ready(PyQt_PyObject)'),
                               self._on_board_view_new_headlines_ready)
                thread.start()
                
                self.thread_pool.append(thread)
            else:
                loading_board_view = ui.LoadingBoardView(self.view.main_window)
                self.view.main_window.set_content(loading_board_view)
            
                thread = retrieveheadlinesthread.RetrieveHeadlinesThread(board_iden)
                thread.connect(thread, QtCore.SIGNAL('ready(PyQt_PyObject)'),
                               self._on_board_view_click_board_ready)            
                thread.start()
                
                self.thread_pool.append(thread)
    
    def _on_board_view_new_headlines_ready(self, result):
        self.config.boards_cache.update_last_retrieved(result.board)
        
        if isinstance(self.view.main_window.content, ui.BoardView):
            board_view = self.view.main_window.content
        
            if result.board_iden == board_view.board_iden:    
                board_view.update_threadlist(result.board)
        
        self.view.main_window.update_board_tree(result.board_iden)
        
    def _on_board_view_click_board_ready(self, result):
        self.config.boards_cache.update_last_retrieved(result.board)
        
        board_view = ui.BoardView(self.view.main_window, result.board_iden, self.config)
        board_view.update_threadlist(result.board)
        
        board_view.connect(board_view.get_splitter(),
                           QtCore.SIGNAL('splitterMoved(int,int)'),
                           self._on_board_view_splitter_moved)

        board_view.connect(board_view.thread_list.get_tree_widget(),
                           QtCore.SIGNAL('itemClicked(QTreeWidgetItem *, int)'),
                           self._on_thread_list_item_click)
        
        # Display the board view in the main window
        self.view.main_window.set_content(board_view)
            
    def _on_board_tree_update_site(self, site_iden):
        """When the user specifies to update all boards in a site via the
        right click menu."""
        for board_iden in site_iden.board_idens:
            self._on_board_tree_update_board(board_iden)
        
    def _on_board_tree_mark_site_as_read(self, site_iden):
        """When the user specifies to mark all boards in a site as read via
        the right-click menu."""
        for board_iden in site_iden.board_idens:
            self._on_board_tree_mark_board_as_read(board_iden)

    def _on_board_tree_update_board(self, board_iden):
        """When the user specifies to force an update of a board."""
        # Note: the callback method used here will only update the GUI if the
        # board is being displayed, so it is safe to use here.
        thread = retrieveheadlinesthread.RetrieveHeadlinesThread(board_iden)
        thread.connect(thread, QtCore.SIGNAL('ready(PyQt_PyObject)'),
                       self._on_board_view_new_headlines_ready)
        thread.start()

        self.thread_pool.append(thread)                

    def _on_board_tree_mark_board_as_read(self, board_iden):
        """When the user specifies to mark board as read via the right click menu."""
        last_retrieved = self.config.boards_cache.get_last_retrieved(board_iden)
        
        if last_retrieved and isinstance(self.view.main_window.content, ui.BoardView):
            self.view.main_window.content.update_threadlist(last_retrieved.to_board())
        
        self.view.main_window.update_board_tree(board_iden)
        
    def _on_board_view_splitter_moved(self, pos, idx):
        self.config.threadlist_height = pos
        
    def _on_thread_list_item_click(self, tree_widget_item, col):
        # Display this thread in the thread view 
        board_iden = tree_widget_item.board_iden
        thread_num = tree_widget_item.thread_num
        
        board = model.Board(board_iden)
        thread_url = board.get_thread_url(thread_num, 'l40')
        
        self.view.main_window.content.update_threadview_url(thread_num, thread_url)
        
        # Connect with the signals in the thread web view
        thread_view = self.view.main_window.content.thread_view
        
        thread_view.page().setLinkDelegationPolicy(QtWebKit.QWebPage.DelegateExternalLinks)
        thread_view.connect(thread_view.get_web_view(),
                            QtCore.SIGNAL('linkClicked(const QUrl&)'),
                            self._on_thread_view_link_clicked)
        
        thread_view.connect(thread_view.get_web_view(),
                            QtCore.SIGNAL('urlChanged(QUrl)'),
                            self._on_thread_view_url_changed)
        
        # Set the font in the thread list to not be bold, as we're reading this thread
        font = tree_widget_item.font(0)
        font.setBold(False)
        tree_widget_item.setFont(0, font)
        tree_widget_item.setFont(1, font)
        tree_widget_item.setFont(2, font)
        tree_widget_item.setFont(3, font)    
        
        # Update the (n) tag in the board tree
        self.config.boards_cache.mark_thread_as_read(board_iden, thread_num)
        self.view.main_window.update_board_tree(board_iden)

    def _on_thread_view_link_clicked(self, qurl, links_opened={}):
        """Triggered when the user clicks a link inside a thread view."""
        url = str(qurl.toString())
        
        # First, we block attempts to reach the board page to prevent leaving
        # the sandbox.
        board = model.Board(self.view.main_window.content.board_iden)
        if url in board.get_board_urls():
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
            board_view.update_threadview_url(thread_num, url)
        else:
            # There is a nasty bug in Qt webkit that is for some reason triggering
            # linkClicked(QUrl&) multiple times for a single click. To work around
            # this we prevent opening the link more than once in 50ms.
            if url in links_opened and time.time() - links_opened[url] < .05:                
                pass  # Block opening link
            else:
                links_opened[url] = time.time()
                webbrowser.open(url)
    
    def _on_thread_view_url_changed(self, qurl):
        """Triggered when the URL changes.
        
        Note that if the URL is changed due a user clicking a link, the method 
        _on_thread_view_link_clicked is called first.
        """
        # What we do here is intercept loads of the board URL, assuming they
        # are redirects after the user has posted. Instead, we send the user
        # back to the thread they just posted in.
        board_view = self.view.main_window.content 
        thread_view = board_view.thread_view
        url =  str(qurl.toString())
        
        board = model.Board(board_view.board_iden)        
        
        if url in board.get_board_urls():
            thread_num = thread_view.thread_num    
            target_url = board.get_thread_url(thread_num, 'l5')        
            board_view.update_threadview_url(thread_num, target_url)
            
            # Update cache so we don't think our own post is new
            self.config.boards_cache.inc_thread_num_posts(board_view.board_iden,
                                                          thread_num, 1)
            
    def _on_exit(self):
        """Shuts down the program."""
        self.config.sidebar_width = self.view.main_window.vsplitter.sizes()[0]
        
        self.config.main_window_size = (self.view.main_window.size().width(),
                                        self.view.main_window.size().height())
        
        self.config.Save()

        self.app.quit()
        
