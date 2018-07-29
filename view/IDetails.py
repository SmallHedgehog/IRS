from PyQt5.QtWidgets import QDialog, QLabel, QHBoxLayout
from PyQt5.QtWidgets import QPushButton, QVBoxLayout, QFrame
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QPixmap


_style = """
QPushButton{
        border-radius: 5px;
        border: none;
        width: 70px;
        height: 30px;
        font: 75 11pt "Consolas";
}
QPushButton:enabled {
        background: rgb(80, 81, 86);
        color: white;
}
QPushButton:!enabled {
        background: rgb(80, 81, 86);
        color: rgb(200, 200, 200);
}
QPushButton:enabled:hover{
        background: rgb(85, 86, 91);
}
QPushButton:enabled:pressed{
        background: rgb(80, 81, 96);
}
"""

class ImageDetails(QDialog):
    def __init__(self, parent, _image, _args):
        super(ImageDetails, self).__init__(parent)
        self.image = _image
        self.args = _args
        self.parent = parent
        self._setup()
        self._connect()
        self.setWindowTitle('Image Details')
        # self.setWindowFlag(Qt.FramelessWindowHint)

    def _setup(self):
        assert self.args.scale > 0

        self.retrival = QPushButton('Search')
        self.retrival.setStyleSheet(_style)
        self.showImage = QLabel(self)
        pix = QPixmap(self.image)

        self.ISize = QLabel('Size: ' +
            str(pix.width()) + 'x' + str(pix.height()))
        self.IPath = QLabel('Source:' + self.image)

        if pix.width() <= self.args.margin \
            and pix.height() <= self.args.margin:
            pass
        else:
            pix = pix.scaled(QSize(
                pix.width() * self.args.scale,
                pix.height() * self.args.scale
            ))
        self.showImage.setPixmap(pix)
        self.showImage.setScaledContents(True)

        vbox = QVBoxLayout(self)
        vbox.addWidget(self.showImage)

        vbox.addWidget(self.parent.hline())

        hbox = QHBoxLayout()
        hbox.addStretch()
        hbox.addWidget(self.ISize)
        hbox.addStretch()
        vbox.addLayout(hbox)
        # vbox.addWidget(self.IPath)
        vbox.addWidget(self.retrival)

    def _slot_close(self):
        self.close()

    def _connect(self):
        self.retrival.clicked.connect(self.parent.slot_detail_search)
        self.retrival.clicked.connect(self._slot_close)
