#!/usr/bin/python

import os
import sys
from PyQt4 import QtCore
from PyQt4 import QtGui
from zonu import controller
from zonu import model
from zonu import ui
from zonu.utils import logging


def main():
    app = QtGui.QApplication(sys.argv)

    config_dir_path = os.path.join(str(QtCore.QDir.homePath()), '.zonu')
    config = model.ConfigDir(config_dir_path)

    logging.set_level(config.debug_level)

    view = ui.View(config)
    
    app_controller = controller.Controller(app, view, config)
    app_controller.initialize()
    app_controller.bind_view()
    app_controller.start_bg_tasks()
    
    sys.exit(app.exec_())
    
    
if __name__ == '__main__':
    main()
