from PyQt5.QtWidgets import *
from PyQt5.QtCore import *


class ResizeDlg(QDialog):
    def __init__(self, width, height, parent=None):
        super().__init__(parent)

        widthLabel = QLabel("&Width:")
        self.widthSpinBox = QSpinBox()
        widthLabel.setBuddy(self.widthSpinBox)
        self.widthSpinBox.setRange(4, width * 4)
        self.widthSpinBox.setValue(width)
        self.heightLabel = QLabel("&Height:")
        self.heightSpinBox = QSpinBox()
        self.heightSpinBox.setRange(4, height * 4)
        self.heightSpinBox.setValue(height)
        self.heightLabel.setBuddy(self.heightSpinBox)
        buttonbox = QDialogButtonBox(QDialogButtonBox.Ok|QDialogButtonBox.Cancel)
        layoutbox = QGridLayout()
        layoutbox.addWidget(widthLabel, 0,0)
        layoutbox.addWidget(self.widthSpinBox, 0, 1)
        layoutbox.addWidget(self.heightLabel, 1,0)
        layoutbox.addWidget(self.heightSpinBox, 1,1)

        layoutbox.addWidget(buttonbox, 2,0)
        self.setLayout(layoutbox)
        buttonbox.accepted.connect(self.accept)
        buttonbox.rejected.connect(self.reject)

        self.setWindowTitle("Image Changer - Resize")

    def result(self):
        return self.widthSpinBox.value(), self.heightSpinBox.value()


if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    form = ResizeDlg(50, 100)
    form.show()
    sys.exit(app.exec_())

