#!/usr/bin/env python3
# Copyright (c) 2008-10 Qtrac Ltd. All rights reserved.
# This program or module is free software: you can redistribute it and/or
# modify it under the terms of the GNU General Public License as published
# by the Free Software Foundation, either version 2 of the License, or
# version 3 of the License, or (at your option) any later version. It is
# provided for educational purposes and is distributed in the hope that
# it will be useful, but WITHOUT ANY WARRANTY; without even the implied
# warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See
# the GNU General Public License for more details.

import os
import platform
import sys

from PyQt5.QtCore import QFile, Qt, QSettings, QByteArray, QFileInfo, QTimer, QT_VERSION_STR, PYQT_VERSION_STR
# from PyQt5.QtCore import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtPrintSupport import *
from PyQt5.QtWidgets import *

import helpform
import newimagedlg
import resizemenu
import qrc_resources

__version__ = "1.0.1"


class MainWindow(QMainWindow):
    """
     Main window style apps are created by subclassing QMainWindow
     The window has a single widget (which may be composite and so
     contain other widgets) as its central widget.

    """

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)

        self.image = QImage()
        self.dirty = False  # No unsaved changes exist
        self.filename = None
        self.mirroredvertically = False
        self.mirroredhorizontally = False

        # A QLabel can display plain text, or HTML, or an image in any
        # of the image formats that PyQt supports
        self.imageLabel = QLabel()

        self.imageLabel.setMinimumSize(200, 200)
        self.imageLabel.setAlignment(Qt.AlignCenter)
        self.imageLabel.setContextMenuPolicy(Qt.ActionsContextMenu)
        # Set the imageLabel where the image file will be viewed
        self.setCentralWidget(self.imageLabel)

        logDockWidget = QDockWidget("Log", self)
        logDockWidget.setObjectName("LogDockWidget")
        logDockWidget.setAllowedAreas(Qt.LeftDockWidgetArea|
                                      Qt.RightDockWidgetArea)
        self.listWidget = QListWidget()
        logDockWidget.setWidget(self.listWidget) # add the listWidget to the logDockWidget docking area
        self.addDockWidget(Qt.RightDockWidgetArea, logDockWidget)

        self.printer = None

        self.sizeLabel = QLabel()
        self.sizeLabel.setFrameStyle(QFrame.StyledPanel|QFrame.Sunken)
        status = self.statusBar()
        status.setSizeGripEnabled(False)
        status.addPermanentWidget(self.sizeLabel)
        status.showMessage("Ready", 5000)

        fileNewAction = self.createAction("&New...", self.fileNew,
                                          QKeySequence.New, "filenew", "Create an image file")
        fileOpenAction = self.createAction("&Open...", self.fileOpen,
                                           QKeySequence.Open, "fileopen",
                                           "Open an existing image file")
        fileSaveAction = self.createAction("&Save", self.fileSave,
                                           QKeySequence.Save, "filesave", "Save the image")
        fileSaveAsAction = self.createAction("Save &As...",
                                             self.fileSaveAs, icon="filesaveas",
                                             tip="Save the image using a new name")
        filePrintAction = self.createAction("&Print", self.filePrint,
                                            QKeySequence.Print, "fileprint", "Print the image")
        fileQuitAction = self.createAction("&Quit", self.close,
                                           "Ctrl+Q", "filequit", "Close the application")
        editInvertAction = self.createAction("&Invert",
                                             self.editInvert, "Ctrl+I", "editinvert",
                                             "Invert the image's colors", True, "toggled(bool)")
        editSwapRedAndBlueAction = self.createAction("Sw&ap Red and Blue",
                                                     self.editSwapRedAndBlue, "Ctrl+A", "editswap",
                                                     "Swap the image's red and blue color components", True,
                                                     "toggled(bool)")
        editZoomAction = self.createAction("&Zoom...", self.editZoom,
                                           "Alt+Z", "editzoom", "Zoom the image")
        editResizeAction = self.createAction("&Resize...", self.editResize,
                                           "Ctrl+R", "editresize", "Resize the image")

        mirrorGroup = QActionGroup(self)
        editUnMirrorAction = self.createAction("&Unmirror",
                                               self.editUnMirror, "Ctrl+U", "editunmirror",
                                               "Unmirror the image", True, "toggled(bool)")
        mirrorGroup.addAction(editUnMirrorAction)
        editMirrorHorizontalAction = self.createAction(
            "Mirror &Horizontally", self.editMirrorHorizontal,
            "Ctrl+H", "editmirrorhoriz",
            "Horizontally mirror the image", True, "toggled(bool)")
        mirrorGroup.addAction(editMirrorHorizontalAction)
        editMirrorVerticalAction = self.createAction(
            "Mirror &Vertically", self.editMirrorVertical,
            "Ctrl+V", "editmirrorvert",
            "Vertically mirror the image", True, "toggled(bool)")
        mirrorGroup.addAction(editMirrorVerticalAction)
        editUnMirrorAction.setChecked(True)
        helpAboutAction = self.createAction("&About RoastMaster Companion",
                                            self.helpAbout)
        helpHelpAction = self.createAction("&Help", self.helpHelp,
                                           QKeySequence.HelpContents)

        self.fileMenu = self.menuBar().addMenu("&File")
        self.fileMenuActions = (fileNewAction, fileOpenAction,
                                fileSaveAction, fileSaveAsAction, None, filePrintAction,
                                fileQuitAction)
        # self.connect(self.fileMenu, SIGNAL("aboutToShow()"),
        #              self.updateFileMenu)
        self.fileMenu.aboutToShow.connect(self.updateFileMenu)
        editMenu = self.menuBar().addMenu("&Edit")
        self.addActions(editMenu, (editInvertAction,
                                   editSwapRedAndBlueAction, editZoomAction, editResizeAction))
        mirrorMenu = editMenu.addMenu(QIcon(":/editmirror.png"),
                                      "&Mirror")
        self.addActions(mirrorMenu, (editUnMirrorAction,
                                     editMirrorHorizontalAction, editMirrorVerticalAction))
        helpMenu = self.menuBar().addMenu("&Help")
        self.addActions(helpMenu, (helpAboutAction, helpHelpAction))

        fileToolbar = self.addToolBar("File")
        fileToolbar.setObjectName("FileToolBar")
        self.addActions(fileToolbar, (fileNewAction, fileOpenAction,
                                      fileSaveAsAction))
        editToolbar = self.addToolBar("Edit")
        editToolbar.setObjectName("EditToolBar")
        self.addActions(editToolbar, (editInvertAction,
                                      editSwapRedAndBlueAction, editUnMirrorAction,
                                      editMirrorVerticalAction, editMirrorHorizontalAction))
        self.zoomSpinBox = QSpinBox()
        self.zoomSpinBox.setRange(1, 400)
        self.zoomSpinBox.setSuffix(" %")
        self.zoomSpinBox.setValue(100)
        self.zoomSpinBox.setToolTip("Zoom the image")
        self.zoomSpinBox.setStatusTip(self.zoomSpinBox.toolTip())
        self.zoomSpinBox.setFocusPolicy(Qt.NoFocus)
        # self.connect(self.zoomSpinBox,
        #              SIGNAL("valueChanged(int)"), self.showImage)
        self.zoomSpinBox.valueChanged.connect(self.showImage)
        editToolbar.addWidget(self.zoomSpinBox)

        self.addActions(self.imageLabel, (editInvertAction,
                                          editSwapRedAndBlueAction, editUnMirrorAction,
                                          editMirrorVerticalAction, editMirrorHorizontalAction))

        self.resetableActions = ((editInvertAction, False),
                                 (editSwapRedAndBlueAction, False),
                                 (editUnMirrorAction, True))

        settings = QSettings()
        self.recentFiles = settings.value("RecentFiles") or []
        self.restoreGeometry(settings.value("MainWindow/Geometry",
                                            QByteArray()))
        self.restoreState(settings.value("MainWindow/State",
                                         QByteArray()))

        self.setWindowTitle("Image Changer")
        self.updateFileMenu()
        QTimer.singleShot(0, self.loadInitialFile)

    # editZoomAction = self.createAction("&Zoom...", self.editZoom,
    #                                    "Alt+Z", "editzoom", "Zoom the image")

    def createAction(self, text, slot=None, shortcut=None, icon=None,
                     tip=None, checkable=False, signal="triggered()"):
        print("createAction {}, {}, {}, {}, {}, {}, {}".format(text, slot, shortcut, icon, tip, checkable, signal))
        # self.signal = signal
        # print("createAction")
        action = QAction(text, self)
        if icon is not None:
            action.setIcon(QIcon(":/{}.png".format(icon)))
        if shortcut is not None:
            action.setShortcut(shortcut)
        if tip is not None:
            action.setToolTip(tip)
            action.setStatusTip(tip)
        if slot is not None:
            #   Below is the original code from PyQt4
            # self.connect(action, SIGNAL(signal), slot)
            #   Below I tried to substitute the new style signal for PyQt5
            #   but signal is not recognized as the value of signal passed to
            #   the method so I received Traceback
            #   "AttributeError: 'QAction' object has no attribute 'signal'
            # action.signal.connect(slot)
            if signal == "triggered()":
                action.triggered.connect(slot)
            elif signal == "toggled(bool)":
                action.toggled[bool].connect(slot)
            else:
                print("No signal provided")


        if checkable:
            action.setCheckable(True)
        return action

    def addActions(self, target, actions):
        # print("addActions: {}/{}".format(target, actions))
        for action in actions:
            if action is None:
                target.addSeparator()
            else:
                target.addAction(action)


    def closeEvent(self, event):
        if self.okToContinue():
            settings = QSettings()
            settings.setValue("LastFile", self.filename)
            settings.setValue("RecentFiles", self.recentFiles or [])
            settings.setValue("MainWindow/Geometry", self.saveGeometry())
            settings.setValue("MainWindow/State", self.saveState())
        else:
            event.ignore()


    def okToContinue(self):
        if self.dirty:
            reply = QMessageBox.question(self,
                                         "RoastMaster Companion - Unsaved Changes",
                                         "Save unsaved changes?",
                                         QMessageBox.Yes|QMessageBox.No|QMessageBox.Cancel)
            if reply == QMessageBox.Cancel:
                return False
            elif reply == QMessageBox.Yes:
                return self.fileSave()
        return True


    def loadInitialFile(self):
        print("loadInitialFile")
        settings = QSettings()
        fname = settings.value("LastFile")
        # if fname and os.access(fname, os.F_OK):
        if fname and QFile.exists(fname):
            self.loadFile(fname)


    def updateStatus(self, message):
        print("updateStatus")
        self.statusBar().showMessage(message, 5000)
        self.listWidget.addItem(message)
        if self.filename:
            self.setWindowTitle("Image Changer - {}[*]".format(
                QFileInfo(self.filename).fileName()))
            # os.path.basename(self.filename)))
        elif not self.image.isNull():
            self.setWindowTitle("Image Changer - Unnamed[*]")
        else:
            self.setWindowTitle("Image Changer[*]")
        self.setWindowModified(self.dirty)


    def updateFileMenu(self):
        self.fileMenu.clear()
        self.addActions(self.fileMenu, self.fileMenuActions[:-1])
        current = self.filename
        recentFiles = []
        for fname in self.recentFiles:
            if fname != current and QFile.exists(fname):
                recentFiles.append(fname)
        if recentFiles:
            self.fileMenu.addSeparator()
            for i, fname in enumerate(recentFiles):
                action = QAction(QIcon(":/icon.png"),
                                 "&{} {}".format(i + 1, QFileInfo(fname).fileName()), self)
                action.setData(fname)
                # self.connect(action, SIGNAL("triggered()"),
                #              self.loadFile)
                action.triggered.connect(self.loadFile)
                self.fileMenu.addAction(action)
        self.fileMenu.addSeparator()
        self.fileMenu.addAction(self.fileMenuActions[-1])


    def fileNew(self):
        if not self.okToContinue():
            return
        dialog = newimagedlg.NewImageDlg(self)
        if dialog.exec_():
            self.addRecentFile(self.filename)
            self.image = QImage()
            for action, check in self.resetableActions:
                action.setChecked(check)
            self.image = dialog.image()
            self.filename = None
            self.dirty = True
            self.showImage()
            self.sizeLabel.setText("{} x {}".format(self.image.width(),
                                                    self.image.height()))
            self.updateStatus("Created new image")


    def fileOpen(self):
        if not self.okToContinue():
            return
        dir = (os.path.dirname(self.filename)
               if self.filename is not None else ".")
        formats = (["*.{}".format(format.data().decode("ascii").lower())
                   for format in QImageReader.supportedImageFormats()])
        fname = QFileDialog.getOpenFileName(self,
                                            "Image Changer - Choose Image", dir,
                                            "Image files ({})".format(" ".join(formats)))
        print("File Name: {}".format(fname))
        if fname:

            self.loadFile(fname[0])


    def loadFile(self, fname=None):
        if fname is False:
            fname = None
        if fname is None:
            action = self.sender()
            if isinstance(action, QAction):
                fname = action.data()
                print("loadFile filename: {}".format(fname))
                if not self.okToContinue():
                    return
            else:
                print("returning...")
                return
        if fname:
            print("fname {}".format(fname))
            self.filename = None
            image = QImage(fname) #fname[0]

            if image.isNull():
                message = "Failed to read {}".format(fname)
            else:
                self.addRecentFile(fname)
                self.image = QImage()
                for action, check in self.resetableActions:
                    action.setChecked(check)
                self.image = image
                self.filename = fname
                self.showImage()
                self.dirty = False
                self.sizeLabel.setText("{} x {}".format(
                    image.width(), image.height()))
                message = "Loaded {}".format(os.path.basename(fname))
            self.updateStatus(message)


    def addRecentFile(self, fname):
        if fname is None:
            return
        if fname not in self.recentFiles:
            self.recentFiles = [fname] + self.recentFiles[:8]


    def fileSave(self):
        if self.image.isNull():
            return True
        if self.filename is None:
            return self.fileSaveAs()
        else:
            if self.image.save(self.filename, None):
                self.updateStatus("Saved as {}".format(self.filename))
                self.dirty = False
                return True
            else:
                self.updateStatus("Failed to save {}".format(
                    self.filename))
                return False


    def fileSaveAs(self):
        if self.image.isNull():
            return True
        fname = self.filename if self.filename is not None else "."
        formats = (["*.{}".format(format.data().decode("ascii").lower())
                    for format in QImageWriter.supportedImageFormats()])
        fname = QFileDialog.getSaveFileName(self,
                                            "Image Changer - Save Image", fname,
                                            "Image files ({})".format(" ".join(formats)))
        print("In fileSaveAs. Filename: {}".format(fname[0]))
        if fname[0]:
            if "." not in fname[0]:
                fname += ".png"
            self.addRecentFile(fname[0])
            self.filename = fname[0]
            return self.fileSave()
        return False

    def customContextMenuRequested(self, *args, **kwargs):
        super().customContextMenuRequested(*args, **kwargs)

    def setTabOrder(self, QWidget, QWidget_1):
        super().setTabOrder(QWidget, QWidget_1)

    def unifiedTitleAndToolBarOnMac(self):
        return super().unifiedTitleAndToolBarOnMac()

    def filePrint(self):
        if self.image.isNull():
            return
        if self.printer is None:
            self.printer = QPrinter(QPrinter.HighResolution)
            self.printer.setPageSize(QPrinter.Letter)
        form = QPrintDialog(self.printer, self)
        if form.exec_():
            painter = QPainter(self.printer)
            rect = painter.viewport()
            size = self.image.size()
            size.scale(rect.size(), Qt.KeepAspectRatio)
            painter.setViewport(rect.x(), rect.y(), size.width(),
                                size.height())
            painter.drawImage(0, 0, self.image)


    def editInvert(self, on):
        if self.image.isNull():
            return
        self.image.invertPixels()
        self.showImage()
        self.dirty = True
        self.updateStatus("Inverted" if on else "Uninverted")


    def editSwapRedAndBlue(self, on):
        if self.image.isNull():
            return
        self.image = self.image.rgbSwapped()
        self.showImage()
        self.dirty = True
        self.updateStatus(("Swapped Red and Blue"
                           if on else "Unswapped Red and Blue"))


    def editUnMirror(self, on):
        if self.image.isNull():
            return
        if self.mirroredhorizontally:
            self.editMirrorHorizontal(False)
        if self.mirroredvertically:
            self.editMirrorVertical(False)


    def editMirrorHorizontal(self, on):
        if self.image.isNull():
            return
        self.image = self.image.mirrored(True, False)
        self.showImage()
        self.mirroredhorizontally = not self.mirroredhorizontally
        self.dirty = True
        self.updateStatus(("Mirrored Horizontally"
                           if on else "Unmirrored Horizontally"))


    def editMirrorVertical(self, on):
        if self.image.isNull():
            return
        self.image = self.image.mirrored(False, True)
        self.showImage()
        self.mirroredvertically = not self.mirroredvertically
        self.dirty = True
        self.updateStatus(("Mirrored Vertically"
                           if on else "Unmirrored Vertically"))


    def editZoom(self):
        if self.image.isNull():
            return
        percent, ok = QInputDialog.getInt(self,     # This was getInteger in PyQt4
                                          "Image Changer - Zoom", "Percent:",
                                          self.zoomSpinBox.value(), 1, 400)
        if ok:
            self.zoomSpinBox.setValue(percent)

    def editResize(self):
        if self.image.isNull():
            return
        form = resizemenu.ResizeDlg(self.image.width(),
                                   self.image.height(), self)
        if form.exec_():
            width, height = form.result()
            if (width == self.image.width() and
                height == self.image.height()):
                self.statusBar().showMessage("Resized to the same size",
                                             5000)
            else:
                self.image = self.image.scaled(width, height)
                self.showImage()
                self.dirty = True
                size = "{} x {}".format(self.image.width(),
                                          self.image.height())
                self.sizeLabel.setText(size)
                self.updateStatus("Resized to {}".format(size))


    def showImage(self, percent=None):
        if self.image.isNull():
            return
        if percent is None:
            percent = self.zoomSpinBox.value()
        factor = percent / 100.0
        width = self.image.width() * factor
        height = self.image.height() * factor
        image = self.image.scaled(width, height, Qt.KeepAspectRatio)
        self.imageLabel.setPixmap(QPixmap.fromImage(image))


    def helpAbout(self):
        QMessageBox.about(self, "About Image Changer",
                          """<b>Image Changer</b> v {0}
                          <p>Copyright &copy; 2008-10 Qtrac Ltd.
                          All rights reserved.
                          <p>This application can be used to perform
                          simple image manipulations.
                          <p>Python {1} - Qt {2} - PyQt {3} on {4}""".format(
                              __version__, platform.python_version(),
                              QT_VERSION_STR, PYQT_VERSION_STR,
                              platform.system()))


    def helpHelp(self):
        form = helpform.HelpForm("index.html", self)
        form.show()


def main():
    app = QApplication(sys.argv)
    app.setOrganizationName("Qtrac Ltd.")
    app.setOrganizationDomain("qtrac.eu")
    app.setApplicationName("Image Changer")
    app.setWindowIcon(QIcon(":/icon.png"))
    form = MainWindow()
    form.show()
    app.exec_()


main()

