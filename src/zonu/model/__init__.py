#!/usr/bin/python

import world4ch


site_type_mods = {
    'world4ch': world4ch
}


class Board(object):
    """A Board."""
    def __init__(self, board_iden):
        self.board_iden = board_iden
        
        if board_iden.site_iden.site_type in site_type_mods:
            self.mod = site_type_mods[board_iden.site_iden.site_type]
        else:
            raise ValueError('Site type "%s" not implemented.' 
                             % board_iden.site_iden.site_type)

    def GetHeadlines(self):
        headlines = []
        headline_dicts = self.mod.GetHeadlines(self.board_iden)
        
        for headline_dict in headline_dicts:
            headlines.append(Headline(headline_dict['thread_num'],
                                      headline_dict['subject'],
                                      headline_dict['num_posts']))
            
        return headlines


class Headline(object):
    """A headline on a board."""
    def __init__(self, thread_num, subject, num_posts):
        self.thread_num = thread_num
        self.subject = subject
        self.num_posts = num_posts


class SiteIden(object):
    """An identifier for a Site."""
    def __init__(self, name, site_type, title, board_idens):
        self.name = name
        self.site_type = site_type
        self.title = title
        self.board_idens = board_idens
        
    def __hash__(self):
        return hash(self.name)

        
class BoardIden(object):
    """An Identifier for a Board."""
    def __init__(self, site_iden, name, title, extra_info):
        self.site_iden = site_iden
        self.name = name
        self.title = title
        self.extra_info = extra_info
    
    def __hash__(self):
        return hash((self.site_iden, self.name))
        
        
class ConfigFile(object):
    """A Configuration File."""
    
    def __init__(self, file_name):        
        self.main_window_size = (800, 600)
        
        self.all_boards = [
            {'name': 'world4ch',
             'title': 'world4ch',
             'type': 'world4ch',
             'boards': [{'name': 'vip',
                         'title': 'News 4 VIP'},
                        {'name': 'prog',
                         'title': 'Programming'}]},
            {'name': '4ch',
             'title': '4-ch',
             'type': 'kareha',
             'boards':  [{'name': 'general',
                          'title': 'General'}]},
            ]

    def GetSiteIdens(self):
        site_idens = []
        
        for site_dict in self.all_boards:
            board_idens = []
            
            site_iden = SiteIden(site_dict['name'], site_dict['type'],
                                 site_dict['title'], board_idens)
            site_idens.append(site_iden)
            
            for board_dict in site_dict['boards']:
                board_extra = board_dict.copy()
                del board_extra['name']
                del board_extra['title']
                
                board_idens.append(BoardIden(site_iden,
                                             board_dict['name'],
                                             board_dict['title'],
                                             board_extra))
        
        return site_idens
    
    def Save(self):
        pass
    
