#!/usr/bin/python

import sys
from PyQt4 import QtGui
from zonu import controller
from zonu import model
from zonu import ui


def main():
    app = QtGui.QApplication(sys.argv)
    
    config = model.ConfigFile('')
    view = ui.View(config)
    
    app_controller = controller.Controller(app, view, config)
    app_controller.BindView()
    
    sys.exit(app.exec_())
    
    
if __name__ == '__main__':
    main()
