#!/usr/bin/python

import re
import urllib2
import simplejson


def GetHeadlines(board_iden):
    """Gets headlines for the given board."""
    subjects_url = 'http://dis.4chan.org/%s/subject.txt' % board_iden.name
    subjects_data = urllib2.urlopen(subjects_url).read()
    
    headline_dicts = []

    for line in subjects_data.split('\n'):
        toks = line.split('<>')
        
        try:
            subject, name, unused_whatisthis, thread_num, num_posts, unused_last_msg, unused_last_time = toks
        except ValueError:
            continue

        subject = unicode(subject, 'utf-8', 'ignore')
        subject = _Filter(subject)
        thread_num = int(thread_num)
        num_posts = int(num_posts)

        headline_dicts.append({'author': name,
                               'num_posts': num_posts,
                               'subject': subject,
                               'thread_num': thread_num})
    
    return headline_dicts


def GetThread(board_iden, thread_num):
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
    

def _Filter(s):
    s = s.replace('<br/>', '\n')
    s = s.replace('&quot;', '"')

    return s


def GetThreadURL(board_iden, thread_num, restriction):
    return 'http://dis.4chan.org/read/%s/%d/%s' % (board_iden.name, thread_num, restriction)
    