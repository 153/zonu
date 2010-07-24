#!/usr/bin/python

import board
import site


class ConfigDir(object):
    """A Configuration Setup."""
    
    def __init__(self, dir_path):        
        print dir_path
        self.sidebar_width = 175
        self.main_window_size = (800, 600)
        
        self.num_threads_to_list = 40
        
        self.all_boards = [
            {'name': 'world4ch',
             'title': 'world4ch',
             'type': 'world4ch',
             'url': 'http://dis.4chan.org',
             'boards': [{'name': 'vip',
                         'title': 'News 4 VIP'},
                        {'name': 'prog',
                         'title': 'Programming'}]},
            {'name': '4ch',
             'title': '4-ch',
             'type': 'kareha',
             'url': 'http://4-ch.net',
             'boards':  [{'name': 'general',
                          'title': 'General',
                          'rss_url': 'http://4-ch.net/rss/general.rss'}]},
            ]

    def GetSiteIdens(self):
        site_idens = []
        
        for site_dict in self.all_boards:
            board_idens = []
            
            site_iden = site.SiteIden(site_dict['name'], site_dict['type'],
                                      site_dict['title'], site_dict['url'],
                                      board_idens)
            site_idens.append(site_iden)
            
            for board_dict in site_dict['boards']:
                board_extra = board_dict.copy()
                del board_extra['name']
                del board_extra['title']
                
                board_idens.append(board.BoardIden(site_iden,
                                                   board_dict['name'],
                                                   board_dict['title'],
                                                   board_extra))
        
        return site_idens
    
    def Save(self):
        pass
    
    def __setattr__(self, name, value):
        object.__setattr__(self, name, value)
        #print name, value
        