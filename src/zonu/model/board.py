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
        
        if board_iden.site_iden.site_type in site.site_type_mods:
            self.mod = site.site_type_mods[board_iden.site_iden.site_type]
        else:
            raise ValueError('Site type "%s" not implemented.' 
                             % board_iden.site_iden.site_type)

        self.headlines = None

    def GetHeadlines(self):
        """Get the headlines for this board. They will be stored in the
        'headlines' attribute for later use, if needed.
        """
        headlines = []
        headline_dicts = self.mod.GetHeadlines(self.board_iden)
        
        for headline_dict in headline_dicts:
            headlines.append(Headline(headline_dict['thread_num'],
                                      headline_dict['subject'],                                      
                                      headline_dict['num_posts'],
                                      headline_dict['author']))
            
        self.headlines = headlines
        return headlines

    def GetThread(self, thread_num):
        thread_dict = self.mod.GetThread(self.board_iden, thread_num)
                
        return Thread(self.board_iden, thread_dict['subject'],
                      thread_dict['author'],
                      thread_dict['num_posts'])
    
    def GetThreadURL(self, thread_num, restriction=''):
        return self.mod.GetThreadURL(self.board_iden, thread_num, restriction)   
    
    
class Headline(object):
    """A headline on a board."""
    def __init__(self, thread_num, subject, num_posts, author):
        self.thread_num = thread_num
        self.subject = subject
        self.num_posts = num_posts
        self.author = author


class Thread(object):
    
    def __init__(self, board_iden, subject, author, num_posts):
        self.board_iden = board_iden
        self.subject = subject
        self.author = author
        self.num_posts = num_posts
    

class Post(object):
    """A Post in a thread."""
    def __init__(self, num, author, email, comment):
        self.num = num
        self.author = author
        self.email = email
        self.comment = comment
        