#!/usr/bin/python

import world4ch


site_type_mods = {
    'world4ch': world4ch,
}


def GetBoard(site_type, board_name):
    if site_type in site_type_mods:
        return site_type_mods[site_type].Board(board_name)
    else:
        raise ValueError('Site type "%s" not implemented yet.' % site_type)


def GetThread(site_type, board_name, thread_num):
    if site_type in site_type_mods:
        return site_type_mods[site_type].Thread(board_name, thread_num)
    else:
        raise ValueError('Site type "%s" not implemented yet.' % site_type)