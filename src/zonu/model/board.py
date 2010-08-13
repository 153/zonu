#!/usr/bin/python

import site


class BoardIden(object):
    """An Identifier for a Board."""
    def __init__(self, site_iden, name, title, extra_info):
        self.site_iden = site_iden
        self.name = name
        self.title = title
        self.extra_info = extra_info
    
    def __hash__(self):
        return hash((self.site_iden, self.name))

    def __eq__(self, other):
        return (self.site_iden.name == other.site_iden.name
                and self.name == other.name)
    
    def __repr__(self):
        return 'BoardIden(%s, %s, %s, %s)' % (repr(self.site_iden), repr(self.name),
                                              repr(self.title), repr(self.extra_info))
 
class Board(object):
    """A Board."""
    def __init__(self, board_iden):
        self.board_iden = board_iden
        self.headlines = None
        self._set_mod()
    
    def _set_mod(self):
        if self.board_iden.site_iden.site_type in site.site_type_mods:
            self.mod = site.site_type_mods[self.board_iden.site_iden.site_type]
        else:
            raise ValueError('Site type "%s" not implemented.' 
                             % self.board_iden.site_iden.site_type)

    def get_headlines(self):
        """Get the headlines for this board.
        
        They will be stored in the 'headlines' attribute for later use,
        if needed.
        """
        headlines = []
        headline_dicts = self.mod.get_headlines(self.board_iden)
        
        for headline_dict in headline_dicts:
            headlines.append(Headline(headline_dict['thread_num'],
                                      headline_dict['subject'],                                      
                                      headline_dict['num_posts'],
                                      headline_dict['author'],
                                      headline_dict['sort_key']))
            
        self.headlines = headlines
        return headlines

    def get_thread(self, thread_num):
        thread_dict = self.mod.GetThread(self.board_iden, thread_num)
                
        return Thread(self.board_iden,
                      thread_num,
                      thread_dict['subject'],
                      thread_dict['author'],
                      thread_dict['num_posts'])
    
    def get_thread_url(self, thread_num, restriction=''):
        return self.mod.get_thread_url(self.board_iden, thread_num, restriction)   
    
    def get_board_urls(self):
        return self.mod.get_board_urls(self.board_iden)
    
    def __setstate__(self, state):
        """Restart instance from pickled state."""
        for name, value in state.iteritems():
            setattr(self, name, value)
        
        self._set_mod()
        assert hasattr(self, 'mod')
        
    def __getstate__(self):
        """Retrieve state for pickling."""
        state = self.__dict__.copy()
        del state['mod']
        return state


class Headline(object):
    """A headline on a board."""
    def __init__(self, thread_num, subject, num_posts, author, sort_key):
        self.thread_num = thread_num
        self.subject = subject
        self.num_posts = num_posts
        self.author = author
        self.sort_key = sort_key

    def copy(self):
        return Headline(self.thread_num, self.subject, self.num_posts,
                        self.author, self.sort_key)


class Thread(object):
    """A thread on a board."""
    def __init__(self, board_iden, thread_num, subject, author, num_posts):
        self.board_iden = board_iden
        self.thread_num = thread_num
        self.subject = subject
        self.author = author
        self.num_posts = num_posts
