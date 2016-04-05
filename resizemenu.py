from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import sys


class Resizedlg(QDialog):
    def __init__(self):
        super().__init__()

        # self.sizeBox = QComboBox()
        # self.docwidget = QDockWidget()
        self.widthLabel = QLabel("&Width")
        self.widthLabel.setMinimumSize(50,50)
        self.widthSpinBox = QSpinBox()
        self.widthLabel.setBuddy(self.widthSpinBox)
        self.heightLabel = QLabel("&Height")
        self.buttonbox = QDialogButtonBox(QDialogButtonBox.Ok|QDialogButtonBox.Cancel)
        layoutbox = QGridLayout()
        layoutbox.addWidget(self.widthLabel, 0,0)
        layoutbox.addWidget(self.heightLabel, 1,0)

        layoutbox.addWidget(self.buttonbox, 2,2)
        # layoutbox.addWidget(self.docwidget)
        self.setLayout(layoutbox)

        self.setWindowTitle("This is a test")



if __name__ == "__main__":

    app = QApplication(sys.argv)
    form = Resizedlg()
    form.show()
    sys.exit(app.exec_())
