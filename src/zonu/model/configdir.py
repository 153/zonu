#!/usr/bin/python

import cPickle as pickle
import os
import yaml
from zonu.utils import logging
import board
import boardscache
import site


_DEFAULT_CONFIG = dict()
_DEFAULT_CONFIG['general'] = dict()
_DEFAULT_CONFIG['general']['debug_level'] = 'error'
_DEFAULT_CONFIG['general']['last_used_version'] = '0.5'
_DEFAULT_CONFIG['general']['num_threads_to_list'] = 40
_DEFAULT_CONFIG['general']['board_crawl_rate'] = 60
_DEFAULT_CONFIG['ui'] = dict()
_DEFAULT_CONFIG['ui']['sidebar_width'] = 175
_DEFAULT_CONFIG['ui']['main_window_size'] = [800, 600]
_DEFAULT_CONFIG['ui']['threadlist_height'] = 400


_DEFAULT_SITES = {'all_sites':
                   [#{'name': 'world4ch',
                    #'title': 'world4ch',
                    #'type': 'world4ch',
                    #'url': 'http://dis.4chan.org',
                    #'boards': [{'name': 'lounge', 'title': 'Lounge'},
                    #           {'name': 'vip', 'title': 'News 4 VIP'},
                    #           {'name': 'prog', 'title': 'Programming'},
                    #           {'name': 'tech', 'title': 'Technology'}]},
                    {'name': '4ch',
                     'title': '4-ch',
                     'type': 'kareha',
                     'url': 'http://4-ch.net',
                     'boards':  [{'name': 'general', 'title': 'General'},
                                 {'name': 'dqn', 'title': 'DQN'},
                                 {'name': 'code', 'title': 'Programming'}]},
                    
                    {'name': 'saovq',
                     'title': 'SAoVQ',
                     'type': 'kareha',
                     'url': 'http://www.secretareaofvipquality.net',
                     'boards': [{'name': 'saovq', 'title': 'Text BBS'}]},
                    
                    {'name': 'sageru',
                     'title': '6ch',
                     'type': 'kareha',
                     'url': 'http://sageru.org',
                     'boards': [{'name': './', 'title': 'Unholy Citadel'}]},                     
                    ]}


_DEFAULT_BOARDS_CACHE = boardscache.BoardsCache()


class ConfigDir(object):
    """A Configuration Setup."""
    
    _CONFIG_FILE_NAME = 'config.yaml'
    _SITES_FILE_NAME = 'sites.yaml'
    _BOARDS_CACHE_FILE_NAME = 'boards.cache'
    
        
    def __init__(self, dir_path):        
        self.dir_path = dir_path
        
        config_yaml_path = os.path.join(self.dir_path, self._CONFIG_FILE_NAME)
        sites_yaml_path = os.path.join(self.dir_path, self._SITES_FILE_NAME)
        boards_cache_path = os.path.join(self.dir_path, self._BOARDS_CACHE_FILE_NAME)
        
        if not os.path.exists(dir_path):
            os.mkdir(self.dir_path)
            print 'Created', self.dir_path        
            
        if not os.path.exists(config_yaml_path):
            yaml.dump(_DEFAULT_CONFIG, open(config_yaml_path, 'w'))
            print 'Created', config_yaml_path    
        
        if not os.path.exists(sites_yaml_path):
            yaml.dump(_DEFAULT_SITES, open(sites_yaml_path, 'w'))        
            print 'Created', sites_yaml_path 
        
        if not os.path.exists(boards_cache_path):
            pickle.dump(_DEFAULT_BOARDS_CACHE, open(boards_cache_path, 'w'))
            print 'Created', boards_cache_path

        zonu_dict = yaml.load(open(config_yaml_path))
        self.general = zonu_dict['general']
        self.ui = zonu_dict['ui']
        
        boards_dict = yaml.load(open(sites_yaml_path))
        self.all_sites =  boards_dict['all_sites']

        boards_cache = pickle.load(open(boards_cache_path))
        self.boards_cache = boards_cache
        
    def GetSiteIdens(self):
        site_idens = []
        
        for site_dict in self.all_sites:
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
        """Save the configuration."""
        config_yaml_path = os.path.join(self.dir_path, self._CONFIG_FILE_NAME)
        sites_yaml_path = os.path.join(self.dir_path, self._SITES_FILE_NAME)
        boards_cache_path = os.path.join(self.dir_path, self._BOARDS_CACHE_FILE_NAME)
        
        config_dict = dict()
        config_dict['general'] = self.general
        config_dict['ui'] = self.ui
        yaml.dump(config_dict, open(config_yaml_path, 'w'))
        
        boards_dict = dict()
        boards_dict['all_sites'] = self.all_sites
        yaml.dump(boards_dict, open(sites_yaml_path, 'w'))
        
        pickle.dump(self.boards_cache, open(boards_cache_path, 'w'))


    # General Properties
    # ----------------------------------------------------------------------

    # Debug level
    @property
    def debug_level(self):
        return self.general['debug_level']

    @debug_level.setter
    def debug_level(self, value):
        if level in logging.ALL_LEVELS:
            self.general['debug_level'] = level
        else:
            logging.error('Refusing to set invalid log level: %s' % value)

    # Number of threads to list
    @property
    def num_threads_to_list(self):
        return self.general['num_threads_to_list']

    @num_threads_to_list.setter
    def num_threads_to_list(self, value):
        if isinstance(value, int):
            self.general['num_threads_to_list'] = value
        else:
            logging.error('Refusing to set non-int num_threads_to_list"')

    # Board crawl rate
    @property
    def board_crawl_rate(self):
        return self.general['board_crawl_rate']
    
    @board_crawl_rate.setter
    def board_crawl_rate(self, value):
        if isinstance(board_crawl_rate, int):
            self.general['board_crawl_rate'] = value
        else:
            logging.error('Refusing to set non-int board_crawl_rate')

    # UI Properties
    # ----------------------------------------------------------------------

    # The sidebar width
    @property
    def sidebar_width(self):
        return self.ui['sidebar_width']

    @sidebar_width.setter
    def sidebar_width(self, value):
        if isinstance(value, int):
            self.ui['sidebar_width'] = value
        else:
            logging.error('Refusing to set non-int sidebar width')

    # The main window size
    @property
    def main_window_size(self):
        return self.ui['main_window_size']

    @main_window_size.setter
    def main_window_size(self, value):
        if not isinstance(value, tuple):
            logging.error('Refusing to set non-tuple main window size')
            return

        if len(value) != 2:
            logging.error('Refusing to set main window size where '
                          'len(size) != 2')
            return

        if not (isinstance(value[0], int) and isinstance(value[1], int)):
            logging.error('Refusing to set main window size where '
                          'width and height are not ints')
            return

        self.ui['main_window_size'] = value
    
    # Thread list height
    @property
    def threadlist_height(self):
        return self.ui['threadlist_height']

    @threadlist_height.setter
    def threadlist_height(self, value):
        if isinstance(value, int):
            self.ui['threadlist_height'] = value
        else:
            logging.error('Refusing to set non-int threadlist height.')
