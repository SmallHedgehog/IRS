from PyQt5.QtWidgets import QListWidgetItem
from PyQt5.QtGui import QIcon


class ImageItem(QListWidgetItem):
    def __init__(self, QIcon, _image):
        super(ImageItem, self).__init__(QIcon, '')
        self._image = _image
        self._rank = 0
        self._score = 0.0

    @property
    def rank(self):
        return self._rank

    @property
    def score(self):
        return self._score

    @property
    def image(self):
        return self._image

    def setRank(self, _rank):
        self._rank = _rank

    def setSore(self, _score):
        self._score = _score
