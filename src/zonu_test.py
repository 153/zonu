#!/usr/bin/python

"""Unit tests for the zonu package."""

import unittest
import sys
from PyQt4 import QtGui
import zonu
try:
    import mox
except ImportError:
    print 'Your nead PyMox to run these unit tests. You can find it at:'
    print 'http://code.google.com/p/pymox/'
    sys.exit(0)


class ControllerTest(unittest.TestCase):

    def setUp(self):
        self.mocker = mox.Mox()
        self.app = self.mocker.CreateMock(QtGui.QApplication)
        self.view = self.mocker.CreateMock(zonu.ui.View)
        self.config = self.mocker.CreateMock(zonu.model.ConfigDir)

    def testInitializer(self):
        # Create some site idens to use.
        site_idens = []        

        world4ch = zonu.model.SiteIden('world4ch', 'world4ch', 'World4ch',
                                       'http://dis.4chan.org', [])
        world4ch.board_idens.append(zonu.model.BoardIden(world4ch, 'prog', 'Programming', {}))        
        site_idens.append(world4ch)

        self.config.GetSiteIdens().AndReturn(site_idens)

        self.config.boards_cache = {'last_retrieved': {},
                                    'last_read': {}}
        self.mocker.ReplayAll()
        controller = zonu.controller.Controller(self.app, self.view, self.config)
        self.mocker.VerifyAll()

    def testBindView(self):
        pass

if __name__ == '__main__':
    unittest.main()
                             
