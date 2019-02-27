from PyQt5.QtWidgets import QAbstractButton
from PyQt5.QtGui import QPainter

class PicButton(QAbstractButton):
    #source : https://stackoverflow.com/questions/2711033/how-code-a-image-button-in-pyqt
    #13.01.2019
    def __init__(self, pixmap,size,parent=None):
        super(PicButton, self).__init__(parent)
        self.pixmap = pixmap
        self.size = size

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.drawPixmap(event.rect(), self.pixmap)

    def sizeHint(self):
        return self.size