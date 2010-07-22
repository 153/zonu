#!/usr/bin/python

from PyQt4 import QtGui


class ThreadView(QtGui.QScrollArea):
    
    def __init__(self, parent, config):
        QtGui.QScrollArea.__init__(self, parent)  
        self.config = config
        self.label = QtGui.QLabel(self)
        
    def _Update(self, thread):
        label_lines = []
        
        for post in thread.posts:
            label_lines.append('%d: %s' % (post.num, post.comment))
            
        label_text = u'\n\n'.join(label_lines)
        self.label.setText(label_text)
        
        self.setWidget(self.label)
        