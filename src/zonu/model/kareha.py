#!/usr/bin/python

import itertools
import re
import simplejson
import sys
import time
import urllib2
import urlparse
from xml.etree import ElementTree
from zonu.utils import logging


def get_headlines(board_iden):
    # We have to first download the board to extract the RSS url, because
    # some sites (like 4-ch) have them in non-default locations.
    board_url = '%s/%s' % (board_iden.site_iden.url, board_iden.name)
    html_data = urllib2.urlopen(board_url).read()
    
    m = re.search('<link rel=\"alternate\" title=\"RSS feed\" href=\"(.*)\" type=\"application\/rss\+xml\"( *)/>',
                  html_data)
    rss_link = m.group(1)
    
    if rss_link.startswith('/'):
        site_url_parsed = urlparse.urlparse(board_iden.site_iden.url)    
        rss_url = '%s://%s%s' % (site_url_parsed.scheme,
                                 site_url_parsed.netloc,
                                 rss_link)
    else:
        rss_url = '%s/%s' % (board_iden.site_iden.url, rss_link)
    
    rss_data = urllib2.urlopen(rss_url).read()
    rss_data = rss_data.replace('&nbsp;', ' ');
    
    # This is a hack to convert SJIS to utf-8 because python XML parsers
    # don't support parsing SJIS, and some sites (like SAoVQ) use SJIS.
    if rss_data.startswith('<?xml version="1.0" encoding="shift_jis"?>'):
        rss_data = unicode(rss_data, 'shiftjis', 'ignore').encode('utf8')
        rss_data = rss_data.replace('<?xml version="1.0" encoding="shift_jis"?>',
                                    '<?xml version="1.0" encoding="utf-8"?>')     
    
    rss  = ElementTree.fromstring(rss_data)
    
    headline_dicts = []    
    items = rss.findall('channel/item')
    
    base_sort_key = int(time.time())
    
    for i, item in enumerate(items):
        author = item.find('author').text
        
        subject = item.find('title').text
        subject = re.sub(' \(\d+\)', '', subject)
        
        m = re.findall('(\d+)', item.find('title').text)
        num_posts = int(m[-1])
        
        m = re.findall('(\d+)', item.find('guid').text)
        thread_num = int(m[-1])

        headline_dicts.append({'author': author,
                               'num_posts': num_posts,
                               'sort_key': base_sort_key + i,
                               'subject': subject,
                               'thread_num': thread_num})

    return headline_dicts


def get_thread(board_iden, thread_num):
    res_url = '%s/%s/res/%d.html' % (board_iden.site_iden.url,
                                     board_iden.name, thread_num)

    logging.debug('Kareha get_thread(%d), fetching: %s' % (thread_num, res_url))

    
    for i in itertools.count():
        try:
            res_html = urllib2.urlopen(res_url).read()
            break
        except (urllib2.URLError, urllib2.HTTPError):
            if i >= 5:
                raise sys.exc_info()[1]

    res_lines = res_html.split('\n')        
    json_meta = res_lines[0][4:-4].replace('\' =>', '\': ')
    json_meta = json_meta.replace('\'', '"')  # TODO(meltingwax) fix this
    json_meta = json_meta.replace('undef', 'null')

    try:
        header_dict = simplejson.loads(json_meta)
    except UnicodeDecodeError:
        header_dict = simplejson.loads(json_meta, encoding='sjis')
    except ValueError:
        print json_meta

    return {'author': header_dict['author'],
            'last_post_time': header_dict['lastmod'],
            'num_posts': header_dict['postcount'],
            'subject': header_dict['title']}
    
    
def get_thread_url(board_iden, thread_num, restriction):    
    thread_url = '%s/%s/kareha.pl/%d/%s' % (board_iden.site_iden.url,
                                            board_iden.name, thread_num,
                                            restriction)
    return thread_url


def get_board_urls(board_iden):
    return ['%s' % board_iden.site_iden.url,
            '%s/' % board_iden.site_iden.url,
            '%s/index.html' % board_iden.site_iden.url,
            '%s/%s' % (board_iden.site_iden.url, board_iden.name),
            '%s/%s/' % (board_iden.site_iden.url, board_iden.name),
            '%s/%s/index.html' % (board_iden.site_iden.url, board_iden.name)]
