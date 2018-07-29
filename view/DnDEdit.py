from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtGui import QDragEnterEvent, QDropEvent


class DndEdit(QLineEdit):
    pic_surfix = ('jpg', 'JPG', 'jpeg', 'JPEG', 'png', 'PNG',
            'bmp', 'BMP')
    def __init__(self):
        super(DndEdit, self).__init__()
        self.setAcceptDrops(True)

    def legal(self, text):
        for surfix in DndEdit.pic_surfix:
            if text.endswith(surfix):
                return True
        return False

    def dragEnterEvent(self, event):
        text = event.mimeData().urls()[0].toLocalFile()
        if self.legal(text):
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        text = event.mimeData().urls()[0].toLocalFile()
        self.clear()
        self.setText(text)
