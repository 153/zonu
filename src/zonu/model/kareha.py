#!/usr/bin/python

import re
import simplejson
import urllib2
import urlparse
from xml.etree import ElementTree


def GetHeadlines(board_iden):
    # We have to first download the board to extract the RSS url, because
    # some sites (like 4-ch) have them in non-default locations.
    board_url = '%s/%s' % (board_iden.site_iden.url, board_iden.name)
    html_data = urllib2.urlopen(board_url).read()
    
    m = re.search('<link rel=\"alternate\" title=\"RSS feed\" href=\"(.*)\" type=\"application\/rss\+xml\" />',
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


def GetThread(board_iden, thread_num):
    res_url = '%s/%s/res/%d.html' % (board_iden.site_iden.url,
                                     board_iden.name, thread_num)
    
    res_html = urllib2.urlopen(res_url).read()
    res_lines = res_html.split('\n')
    
    header_dict = simplejson.loads(res_lines[0][4:-4].replace('\' =>', '\': '))
    
    return {'author': header_dict['author'],
            'num_posts': header_dict['postcount'],
            'subject': header_dict['title']}
    
    
def GetThreadURL(board_iden, thread_num, restriction):    
    thread_url = '%s/%s/kareha.pl/%d/%s' % (board_iden.site_iden.url,
                                            board_iden.name, thread_num,
                                            restriction)
    return thread_url


def GetBoardURLs(board_iden):
    return ['%s/%s' % (board_iden.site_iden.url, board_iden.name),
            '%s/%s/' % (board_iden.site_iden.url, board_iden.name),
            '%s/%s/index.html' % (board_iden.site_iden.url, board_iden.name)]
 