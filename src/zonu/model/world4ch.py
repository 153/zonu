#!/usr/bin/python

import urllib2
import simplejson


def get_headlines(board_iden):
    """Gets headlines for the given board."""
    subjects_url = 'http://dis.4chan.org/%s/subject.txt' % board_iden.name
    subjects_data = urllib2.urlopen(subjects_url).read()
    
    headline_dicts = []

    for line in subjects_data.split('\n'):
        toks = line.split('<>')
        
        if len(toks) != 7:
            continue
        

        subject = toks[0]
        name = toks[1]            
        thread_num = toks[3]
        num_posts = toks[4]
        last_post_time = toks[6]

        subject = unicode(subject, 'utf-8', 'ignore')
        subject = _filter(subject)
        thread_num = int(thread_num)
        num_posts = int(num_posts)
        last_post_time = int(last_post_time)

        headline_dicts.append({'author': name,
                               'num_posts': num_posts,
                               'last_post_time': last_post_time,
                               'subject': subject,
                               'thread_num': thread_num})
    
    return headline_dicts


def get_thread(board_iden, thread_num):
    json_url = 'http://dis.4chan.org/json/%s/%d' % (board_iden.name,
                                                    thread_num)    
    json_data = urllib2.urlopen(json_url).read()        

    try:
        json_dict = simplejson.loads(json_data)
    except ValueError:
        raise Exception()
    
    subject = json_dict['1']['sub']
    author = json_dict['1']['author']
    num_posts = len(json_dict)
            
    return {'author': author,
            'num_posts': num_posts,
            'subject': subject}
    

def _filter(s):
    s = s.replace('<br/>', '\n')
    s = s.replace('&quot;', '"')
    s = s.replace('&#039;', '\'')  # single quote
    return s


def get_thread_url(board_iden, thread_num, restriction):
    return 'http://dis.4chan.org/read/%s/%d/%s' % (board_iden.name, thread_num, restriction)
    
    
def get_board_urls(board_iden):
    return ['http://dis.4chan.org/%s' % board_iden.name,
            'http://dis.4chan.org/%s/' % board_iden.name,
            'http://dis.4chan.org/%s/index.html' % board_iden.name]
