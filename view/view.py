from .DnDEdit import DndEdit

from PyQt5.QtWidgets import QWidget, QLabel, QPushButton, QFileDialog
from PyQt5.QtWidgets import QLineEdit, QListWidget, QListView
from PyQt5.QtWidgets import QListWidgetItem, QScrollBar, QFrame
from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout, QSplitter
from PyQt5.QtGui import QMouseEvent, QPixmap, QIcon, QResizeEvent
from PyQt5.QtCore import QSize


class IRSGUI(QWidget):
    """Image Retrieval System GUI"""
    def __init__(self, args):
        super(IRSGUI, self).__init__()
        self.args = args
        self._setup()
        self._layout()
        self._connect()
        self.setStyleSheet(self.args.style)

    def _connect(self):
        self.select.clicked.connect(self._slot_search)
        self.edit.textChanged.connect(self._slot_edit)

    def _setup(self):
        self.select = QPushButton()
        self.select.setIcon(QIcon(QPixmap(self.args.search)))
        self.select.setStyleSheet(self.args.style)
        self.edit = DndEdit()
        self.edit.setDragEnabled(True)
        self.edit.setStyleSheet(self.args.style)
        self.edit.setMaximumWidth(self.args.lineEdit[1])
        self.edit.setMinimumWidth(self.args.lineEdit[0])
        self.rarea = QListWidget()
        self.rarea.setIconSize(QSize(
            self.args.image_size[0],
            self.args.image_size[1]
        ))
        self.rarea.setResizeMode(QListView.Adjust)
        self.rarea.setFixedWidth(self.args.fix)
        self.rarea.verticalScrollBar().setStyleSheet(self.args.style)
        self.rarea.setViewMode(QListView.IconMode)
        self.rarea.setMovement(QListView.Static)
        self.rarea.setSpacing(self.args.space)
        self.rarea.setStyleSheet(self.args.style)

    def _layout(self):
        hbox = QHBoxLayout()
        hbox.setContentsMargins(self.args.margins[0],
            self.args.margins[1],
            self.args.margins[2],
            self.args.margins[3])
        hbox.addStretch(1)
        hbox.addWidget(self.edit)
        hbox.addWidget((self.select))
        hbox.addStretch(1)

        self.vbox = QVBoxLayout(self)
        self.vbox.addLayout(hbox)
        self.vbox.addWidget(self._hline())
        self.hbox = QHBoxLayout()
        self.hbox.addStretch(1)
        self.hbox.addWidget(self.rarea)
        self.hbox.addStretch(1)
        # self.vbox.addWidget(self.rarea)
        self.vbox.addLayout(self.hbox)

    def _hline(self):
        hline = QFrame()
        hline.setFrameShape(QFrame.HLine)
        hline.setFrameShadow(QFrame.Sunken)
        return hline

    def _create_image(self, image):
        im = QLabel()
        im.setFixedSize(self.args.image_size[0],
            self.args.image_size[1])
        pix = QPixmap(image)
        im.setPixmap(pix)
        im.setScaledContents(True)
        return im

    def _create_icon(self, image):
        pix = QPixmap(image)
        item = QListWidgetItem(QIcon(pix.scaled(QSize(self.args.image_size[0],
            self.args.image_size[1]))), "pass")
        item.setSizeHint(QSize(self.args.image_size[0],
            self.args.image_size[1]))
        return item

    def _slot_edit(self):
        text = self.edit.text()
        if self.edit.legal(text):
            print('_slot_edit->search')

    def _slot_search(self):
        image = QFileDialog.getOpenFileName(directory='.',
                filter='Images (*.png *.jpeg *.bmp *.jpg)',
                parent=self, caption='select a picture to search')
        if image[0] != '':
            self.edit.setText(image[0])

    def images(self):
        for idx in range(self.args.numbers):
            self.rarea.insertItem(idx, self._create_icon('res/icon.png'))
            pass

    def resizeEvent(self, QResizeEvent):
        num = int(self.rarea.size().width()/(self.args.image_size[0]+self.args.space))
        print(self.rarea.size().width() - (num * self.args.image_size[0] + self.args.space))
        print(self.rarea.size())
        print(QResizeEvent.size())
