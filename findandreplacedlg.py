import re
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from ui_findandreplacedlg import Ui_FindAndReplaceDlg


class MyDialog(Ui_FindAndReplaceDlg):
    def __init__(self, text):
        super().setupUi(FindAndReplaceDlg)

    def setupUi(self, FindAndReplaceDlg, text):
        print("In child setupUI")
        self.__text = text
        self.__index = 0
        # self.setupUi(self)
        # self.updateUi()
        self.findButton.clicked.connect(self.test)


    def test(self):
        print("Works...")

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    FindAndReplaceDlg = QDialog()
    ui = MyDialog(text="Hello")
    ui.setupUi(FindAndReplaceDlg, text="Hello2")
    FindAndReplaceDlg.show()
    sys.exit(app.exec_())
