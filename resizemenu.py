from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import sys


class Resizedlg(QDialog):
    def __init__(self, width, height):
        super().__init__()

        # self.sizeBox = QComboBox()
        # self.docwidget = QDockWidget()
        self.widthLabel = QLabel("&Width")
        # self.widthLabel.setMinimumSize(50,50)
        self.widthSpinBox = QSpinBox()
        self.widthSpinBox.setRange(0, width * 4)
        self.widthSpinBox.setValue(width)
        self.widthLabel.setBuddy(self.widthSpinBox)
        self.heightLabel = QLabel("&Height")
        self.heightSpinBox = QSpinBox()
        self.heightSpinBox.setRange(0, height * 4)
        self.heightSpinBox.setValue(height)
        self.heightLabel.setBuddy(self.heightSpinBox)
        buttonbox = QDialogButtonBox(QDialogButtonBox.Ok|QDialogButtonBox.Cancel)
        layoutbox = QGridLayout()
        layoutbox.addWidget(self.widthLabel, 0,0)
        layoutbox.addWidget(self.widthSpinBox, 0, 1)
        layoutbox.addWidget(self.heightLabel, 1,0)
        layoutbox.addWidget(self.heightSpinBox, 1,1)

        layoutbox.addWidget(buttonbox, 2,0)
        self.setLayout(layoutbox)
        # buttonbox.accepted.connect(self.accept)
        # buttonbox.rejected.connect(self.reject)

        self.setWindowTitle("Image Changer - Resize")

    def closeBox(self):
        self.close()

    def result(self):
        return (width, height)



if __name__ == "__main__":
    width = 350
    height = 400
    app = QApplication(sys.argv)
    form = Resizedlg(width, height)
    form.show()
    sys.exit(app.exec_())

