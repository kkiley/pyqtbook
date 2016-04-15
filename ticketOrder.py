from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from datetime import *

from ui_ticketOrder import *

class ticketOrderDlg(QDialog, Ui_ticketOrderDlg):

    def __init__(self, parent=None):
        super(ticketOrderDlg, self).__init__(parent)
        self.setupUi(self)
        print("In child setupUI")

    # It doesn't seem to matter what you put as
    # a parameter for setupUi.
    #     setupUi(self, Dialog):
    #     print("Local setupUI")
        # self.priceSpinBox.setPrefix("$")
        # self.amountSpinBox.setPrefix("$")
        # self.quantitySpinBox.setMaximum(50)
        # self.quantitySpinBox.setValue(1)
        today = QDateTime.currentDateTime()
        self.whenDateTimeEdit.setDateTimeRange(today.addDays(1), today.addYears(2))
        # void QDateTimeEdit::dateTimeChanged(const oQDateTime &datetime)
        # self.myDateTime = QDateTime()
        # print(QDateTime.currentDateTime())
        self.updateUi()
        self.customerLineEdit.setFocus()

    @pyqtSlot("QString")
    def on_customerLineEdit_textEdited(self, text):
        self.updateUi()
    @pyqtSlot("double")
    def on_priceSpinBox_valueChanged(self, value):
        self.updateUi()

    @pyqtSlot("int")
    def on_quantitySpinBox_valueChanged(self, value):
        self.updateUi()

    def updateUi(self):
        # print("updateUI")
        amount = (self.priceSpinBox.value() *
                  self.quantitySpinBox.value())
        enable = bool(self.customerLineEdit.text()) and amount
        self.buttonBox.button(QDialogButtonBox.Ok).setEnabled(enable)
        self.amountLabel.setText("$ {0:.2f}".format(amount))

    def result(self):
        when = self.whenDateTimeEdit.dateTime().toPyDateTime()
        return (self.customerLineEdit.text(), when,
                self.priceSpinBox.value(), self.quantitySpinBox.value())


if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    form = ticketOrderDlg()
    form.show()
    app.exec_()
    print(form.result())
