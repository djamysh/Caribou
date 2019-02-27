from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from dirPath import get_dir_path



class predictionPageLeftNavigationBar(QGroupBox):
    # Bu solda navigasyon barı olacak

    def __init__(self, *args, **kwargs):
        super(predictionPageLeftNavigationBar,self).__init__()
        self.path = get_dir_path()        
        self.setMaximumWidth(250)
        self.setMinimumWidth(250)

        self.setStyleSheet(
            """
            QGroupBox {
                background: qlineargradient(x1: 1, y1: 0, x2:1, y2: 1,
                                 stop: 0 #E6DADA, stop: 1.0 #274046);
                border-style:solid;
                border-color:gray;
                border-width:2px;
                margin-top:1em;
            }
            QGroupBox QGroupBox {
                background-color: green;
            }
            QGroupBox::title {
                subcontrol-origin: padding;
                subcontrol-position: top;
                background: transparent;
                margin-top: -2.5em;
                color:blue;
            }
            """
            )
        self.setTitle("Navigation Bar")
        self.initUI()

    def initUI(self):
        self.mainVerticalLayout = QVBoxLayout()
        self.mainVerticalLayout.setContentsMargins(0,0,0,0)
        
        self.settingIconPath = "{}Images/settings.png".format(self.path)
        self.inputIconPath = "{}Images/input.png".format(self.path)

        self.settingsButton = barButton(iconPath=self.settingIconPath)
        self.settingsButton.setText("Options")
        self.inputButton = barButton(iconPath=self.inputIconPath)
        self.inputButton.setText("Data Entrance")
        self.mainVerticalLayout.addWidget(self.settingsButton)
        self.mainVerticalLayout.addWidget(self.inputButton)        
        self.mainVerticalLayout.addStretch()
        
        self.setLayout(self.mainVerticalLayout)


class barButton(QPushButton):
    def __init__(self,iconPath = "",*args, **kwargs):
        super(barButton,self).__init__()
        self.setStyleSheet("QPushButton { text-align: left;padding-left:4px; }")

        self.iconPixmap = QPixmap(iconPath)
        self.icon = QIcon(self.iconPixmap)
        self.setIconSize(QSize(42,42))
        self.setMinimumHeight(48)
        
        self.font = QFont("Courier")
        self.font.setBold(True)
        self.font.setPixelSize(16)
        self.setFont(self.font)

        self.setIcon(self.icon)

    def initUI(self):
        pass

class mainWidget(QWidget):
    def __init__(self, *args, **kwargs):
        super(mainWidget,self).__init__()
        self.initUI()

    def initUI(self):
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setContentsMargins(0,3,10,0)
        self.leftNavigationBar = predictionPageLeftNavigationBar()

        self.horizontalLayout.addWidget(self.leftNavigationBar)
        self.horizontalLayout.addStretch()
        self.setLayout(self.horizontalLayout)


if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    obj = mainWidget(0)
    obj.show()
    sys.exit(app.exec_())
        