from __future__ import print_function

import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QIcon

from IRS.view.view import IRSGUI
from IRS.config import cfg


if __name__ == '__main__':
    app = QApplication(sys.argv)

    args = cfg()

    w = IRSGUI(args=args)
    w.resize(args.window[0], args.window[1])
    w.setWindowTitle('IRS')
    w.setWindowIcon(QIcon(args.icon))
    w.show()

    sys.exit(app.exec_())
