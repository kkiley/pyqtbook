import re
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from ui_findandreplacedlg import Ui_FindAndReplaceDlg

MAC = True
try:
    from PyQt5.QtGui import qt_mac_set_native_menubar
except ImportError:
    MAC = False

class FindAndReplaceDlg(QDialog, Ui_FindAndReplaceDlg):
    found = pyqtSignal()
    notfound = pyqtSignal()

    def __init__(self, text, parent=None):
        super().__init__(parent)

        print("In child setupUI")
        self.__text = text
        self.__index = 0
        self.setupUi(self)
        if not MAC:
            self.findButton.setFocusPolicy(Qt.NoFocus)
            self.replaceButton.setFocusPolicy(Qt.NoFocus)
            self.replaceAllButton.setFocusPolicy(Qt.NoFocus)
            self.closeButton.setFocusPolicy(Qt.NoFocus)

        self.updateUi()
        # self.findButton.clicked.connect(self.test)

    # @pyqtSlot()
    def on_findLineEdit_textEdited(self, text):
        self.__index = 0
        self.updateUi()

    @pyqtSlot(str)
    def on_findButton_clicked(self):
        regex = self.makeRegex()
        match = regex.search(self.__text, self.__index)
        if match is not None:
            self.__index = match.end()
            self.found.emit(match.start())
        else:
            self.notfound.emit()
    @pyqtSlot(str)
    def on_replaceButton_clicked(self):
        regex = self.makeRegex()
        self.__text = regex.sub(self.replaceLineEdit.text(), self.__text, 1)

    @pyqtSlot(str)
    def on_replaceAllButton_clicked(self):
        regex = self.makeRegex()
        self.__text = regex.sub(self.replaceLineEdit.text(), self.__text)
        print("in replaceAllButtonn")


    def updateUi(self):
        enable = bool(self.findLineEdit.text())
        self.findButton.setEnabled(enable)
        self.replaceButton.setEnabled(enable)
        self.replaceAllButton.setEnabled(enable)

    def text(self):
        return self.__text



    def test(self):
        print("Works...")

if __name__ == "__main__":
    import sys

    text = """US experience shows that, unlike traditional patents,
software patents do not encourage innovation and R&D, quite the
contrary. In particular they hurt small and medium-sized enterprises
and generally newcomers in the market. They will just weaken the market
and increase spending on patents and litigation, at the expense of
technological innovation and research. Especially dangerous are
attempts to abuse the patent system by preventing interoperability as a
means of avoiding competition with technological ability.
--- Extract quoted from Linus Torvalds and Alan Cox's letter
to the President of the European Parliament
http://www.effi.org/patentit/patents_torvalds_cox.html"""


    def found(where):
        print("Found at {}".format(where))


    def nomore():
        print("No more found")

    app = QApplication(sys.argv)
    form = FindAndReplaceDlg(text)
    # ui = Ui_FindAndReplaceDlg()
    # ui.setupUi(FindAndReplaceDlg)
    form.show()
    sys.exit(app.exec_())
    # form = FindAndReplaceDlg(text)
    # form.found.connect(found)
    # form.notfound.connect(nomore)
    # form.show()
    # app.exec_()
    # print(form.text())

