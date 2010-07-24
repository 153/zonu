#!/usr/bin/python

import re
import urllib2
from xml.etree import ElementTree


def GetHeadlines(board_iden):
    
    if 'rss_url' in board_iden.extra_info:
        rss_url = board_iden.extra_info['rss_url']
    else:
        rss_url = '%s/%s/index.rss' % (board_iden.site_iden.url,
                                       board_iden.name)
        
    rss_data = urllib2.urlopen(rss_url).read()
    rss  = ElementTree.fromstring(rss_data)
    
    headline_dicts = []    
    items = rss.findall('channel/item')
    
    for item in items:
        author = item.find('author').text
        
        subject = item.find('title').text
        subject = re.sub(' \(\d+\)', '', subject)
        
        m = re.findall('(\d+)', item.find('title').text)
        num_posts = int(m[-1])
        
        m = re.findall('(\d+)', item.find('guid').text)
        thread_num = int(m[-1])
        
        headline_dicts.append({'author': author,
                               'num_posts': num_posts,
                               'subject': subject,
                               'thread_num': thread_num})
    
    return headline_dicts


def GetThreadURL(board_iden, thread_num, restriction):    
    thread_url = '%s/%s/kareha.pl/%d/%s' % (board_iden.site_iden.url,
                                            board_iden.name, thread_num,
                                            restriction)
    return thread_url
 