#!/usr/bin/env python3

import sys
from frontend import VidPlayer 
from PyQt5 import QtWidgets

def main():
    app = QtWidgets.QApplication(sys.argv)
    win = VidPlayer()

    app.exec_()

if __name__ == '__main__':
    main()
