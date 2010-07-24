#!/usr/bin/python

import os
import sys
from PyQt4 import QtCore
from PyQt4 import QtGui
from zonu import controller
from zonu import model
from zonu import ui


def main():
    app = QtGui.QApplication(sys.argv)
    
    config_dir_path = os.path.join(str(QtCore.QDir.homePath()),
                                   '.zonu')
    config = model.ConfigDir(config_dir_path)
    view = ui.View(config)
    
    app_controller = controller.Controller(app, view, config)
    app_controller.BindView()
    
    sys.exit(app.exec_())
    
    
if __name__ == '__main__':
    main()
