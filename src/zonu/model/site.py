#!/usr/bin/python

import kareha
import world4ch

site_type_mods = {
    'kareha': kareha,
    'world4ch': world4ch
}

class SiteIden(object):
    """An identifier for a Site."""
    def __init__(self, name, site_type, title, url, board_idens):
        self.name = name
        self.site_type = site_type
        self.title = title
        self.url = url
        self.board_idens = board_idens
        
    def __hash__(self):
        return hash(self.name)
