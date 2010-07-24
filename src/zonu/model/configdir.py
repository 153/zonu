#!/usr/bin/python

import os
import yaml
import board
import site


_DEFAULT_CONFIG = dict()
_DEFAULT_CONFIG['general'] = dict()
_DEFAULT_CONFIG['general']['last_used_version'] = '0.5'
_DEFAULT_CONFIG['general']['num_threads_to_list'] = 40
_DEFAULT_CONFIG['ui'] = dict()
_DEFAULT_CONFIG['ui']['sidebar_width'] = 175
_DEFAULT_CONFIG['ui']['main_window_size'] = [800, 600]
_DEFAULT_CONFIG['ui']['threadlist_height'] = 400


_DEFAULT_SITES = {'all_sites':
                   [{'name': 'world4ch',
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
                                  'title': 'General'}]},
                    
                    {'name': 'saovq',
                     'title': 'SAoVQ',
                     'type': 'kareha',
                     'url': 'http://www.secretareaofvipquality.net',
                     'boards': [{'name': 'saovq',
                                 'title': 'Text BBS'}]},
                     
                    ]}



class ConfigDir(object):
    """A Configuration Setup."""
    
    _CONFIG_FILE_NAME = 'config.yaml'
    _SITES_FILE_NAME = 'sites.yaml'
    
    def __init__(self, dir_path):        
        self.dir_path = dir_path
        
        config_yaml_path = os.path.join(self.dir_path, self._CONFIG_FILE_NAME)
        sites_yaml_path = os.path.join(self.dir_path, self._SITES_FILE_NAME)
        
        if not os.path.exists(dir_path):
            os.mkdir(self.dir_path)
            print 'Created', self.dir_path        
            
        if not os.path.exists(config_yaml_path):
            yaml.dump(_DEFAULT_CONFIG, open(config_yaml_path, 'w'))
            print 'Created', config_yaml_path    
        
        if not os.path.exists(sites_yaml_path):
            yaml.dump(_DEFAULT_SITES, open(sites_yaml_path, 'w'))        
            print 'Created', sites_yaml_path 
        
        zonu_dict = yaml.load(open(config_yaml_path))
        self.general = zonu_dict['general']
        self.ui = zonu_dict['ui']
        
        boards_dict = yaml.load(open(sites_yaml_path))
        self.all_sites =  boards_dict['all_sites']

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
        
        config_dict = dict()
        config_dict['general'] = self.general
        config_dict['ui'] = self.ui
        yaml.dump(config_dict, open(config_yaml_path, 'w'))
        
        boards_dict = dict()
        boards_dict['all_sites'] = self.all_sites
        yaml.dump(boards_dict, open(sites_yaml_path, 'w'))
        
    
    def __setattr__(self, name, value):
        object.__setattr__(self, name, value)
        #print name, value
        