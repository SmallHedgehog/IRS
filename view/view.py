from .ImageItem import ImageItem
from .DnDEdit import DndEdit
from .IDetails import ImageDetails
from IRS.calc.dataset import Dataset
from IRS.calc.retrieval import Retrieval, ParisRetrieval

from PyQt5.QtWidgets import QWidget, QLabel, QPushButton, QFileDialog
from PyQt5.QtWidgets import QLineEdit, QListWidget, QListView
from PyQt5.QtWidgets import QListWidgetItem, QScrollBar, QFrame
from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout
from PyQt5.QtGui import QMouseEvent, QPixmap, QIcon, QResizeEvent
from PyQt5.QtGui import QWheelEvent
from PyQt5.QtCore import QSize, Qt

import os


class _STATE(object):
    def __init__(self, args):
        super(_STATE, self).__init__()
        self.is_retrieval = False
        self.retrieval = ParisRetrieval(_args=args)
        self.index = 0

        self.rank_images = []
        self.rank_index = 0

    def reset(self):
        self.rank_images = []
        self.rank_index = 0
        self.is_retrieval = True


class IRSGUI(QWidget):
    """Image Retrieval System GUI"""
    def __init__(self, args):
        super(IRSGUI, self).__init__()
        self.args = args
        self.state = _STATE(self.args)
        self._setup()
        self._layout()
        self._connect()
        self._init_dataset()
        self.setStyleSheet(self.args.style)

    def _init_dataset(self):
        self.dataset = Dataset(self.args.dataset)
        self._images()

    def _connect(self):
        self.select.clicked.connect(self._slot_search)
        self.edit.textChanged.connect(self._slot_edit)
        self.rarea.itemDoubleClicked.connect(self._slot_rarea_dc)
        self.rarea.itemClicked.connect(self._slot_rarea)

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
        self.vbox.addWidget(self.hline())
        self.hbox = QHBoxLayout()
        self.hbox.addStretch(1)
        self.hbox.addWidget(self.rarea)
        self.hbox.addStretch(1)
        # self.vbox.addWidget(self.rarea)
        self.vbox.addLayout(self.hbox)

    def hline(self):
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
        item = ImageItem(QIcon(pix.scaled(QSize(self.args.image_size[0],
            self.args.image_size[1]))), image)
        item.setSizeHint(QSize(self.args.image_size[0],
            self.args.image_size[1]))
        return item

    def _slot_edit(self):
        text = self.edit.text()
        if self.edit.legal(text):
            if os.path.isfile(text):
                self.IRetrieval = text
                self.rarea.clear()
                self.state.reset()
                rank_images = self.state.retrieval.metric(self.IRetrieval)
                if rank_images is None:
                    return
                self.state.rank_images = rank_images
                self.rarea.addItem(self._create_icon(
                    self.IRetrieval
                ))
                self._rank_images(rank_images)

    def _slot_search(self):
        image = QFileDialog.getOpenFileName(directory='.',
                filter='Images (*.png *.jpeg *.bmp *.jpg)',
                parent=self, caption='select a picture to search')
        if image[0] != '':
            self.edit.setText(image[0])

    def _slot_rarea(self, imItem):
        self.IRetrieval = imItem.image
        dialog = ImageDetails(self, imItem.image, self.args)
        dialog.exec_()

    def _slot_rarea_dc(self, imItem):
        pass

    def slot_detail_search(self):
        if hasattr(self, 'IRetrieval'):
            rank_images = self.state.retrieval.metric(self.IRetrieval)
            if rank_images is None:
                return
            self.rarea.clear()
            self.state.reset()
            self.state.rank_images = rank_images
            self._rank_images(rank_images)

    def  _rank_images(self, rank_images):
        for idx in range(self.args.top):
            if idx >= len(rank_images):
                break
            self.rarea.addItem(self._create_icon(
                self.dataset.absolute(rank_images[idx])
            ))
            self.state.rank_index += 1

    def _images(self):
        for idx in range(self.args.start_number):
            if idx >= len(self.dataset):
                break
            self.rarea.insertItem(idx, self._create_icon(
                self.dataset.absolute(self.dataset[idx])
            ))
            self.state.index += 1

    def resizeEvent(self, QResizeEvent):
        pass

    def wheelEvent(self, QWheelEvent):
        para = QWheelEvent.angleDelta().y()
        if para < 0:
            if self.state.is_retrieval:
                index = self.state.rank_index
                dataset = self.state.rank_images
            else:
                index = self.state.index
                dataset = self.dataset
            incre = self.args.incre
            if (index + self.args.incre) > len(dataset):
                incre = len(dataset) - index - 1
            if incre <= 0:
                return
            for incre_idx in range(incre):
                self.rarea.addItem(self._create_icon(
                    self.dataset.absolute(dataset[index + incre_idx])
                ))
                if self.state.is_retrieval:
                    self.state.rank_index += 1
                else:
                    self.state.index += 1
