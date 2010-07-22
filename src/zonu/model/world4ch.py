#!/usr/bin/python

import urllib2


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
        thread_num = int(thread_num)
        num_posts = int(num_posts)

        headline_dicts.append({'author': name,
                               'num_posts': num_posts,
                               'subject': subject,
                               'thread_num': thread_num})
    
    return headline_dicts
    