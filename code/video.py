# Form implementation generated from reading ui file 'video.ui'
#
# Created by: PyQt6 UI code generator 6.4.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(720, 492)
        self.widget = QtWidgets.QWidget(parent=Dialog)
        self.widget.setGeometry(QtCore.QRect(9, 9, 702, 471))
        self.widget.setObjectName("widget")
        self.gridLayout = QtWidgets.QGridLayout(self.widget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.graphicsView = CustomGraphicsView(parent=self.widget)
        self.graphicsView.setMinimumSize(QtCore.QSize(700, 394))
        self.graphicsView.setMaximumSize(QtCore.QSize(700, 394))
        self.graphicsView.setStyleSheet("margin: 0; \n"
"padding: 0;\n"
"border: none;")
        self.graphicsView.setObjectName("graphicsView")
        self.gridLayout.addWidget(self.graphicsView, 0, 0, 2, 2)
        self.widget1 = QtWidgets.QWidget(parent=self.widget)
        self.widget1.setObjectName("widget1")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.widget1)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.ok = QtWidgets.QPushButton(parent=self.widget1)
        self.ok.setObjectName("ok")
        self.horizontalLayout.addWidget(self.ok)
        self.cancel = QtWidgets.QPushButton(parent=self.widget1)
        self.cancel.setObjectName("cancel")
        self.horizontalLayout.addWidget(self.cancel)
        self.btn_play = QtWidgets.QPushButton(parent=self.widget1)
        self.btn_play.setObjectName("btn_play")
        self.horizontalLayout.addWidget(self.btn_play)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.lab_video = QtWidgets.QLabel(parent=self.widget1)
        self.lab_video.setMinimumSize(QtCore.QSize(50, 0))
        self.lab_video.setObjectName("lab_video")
        self.horizontalLayout.addWidget(self.lab_video)
        self.lab_time = QtWidgets.QLabel(parent=self.widget1)
        self.lab_time.setObjectName("lab_time")
        self.horizontalLayout.addWidget(self.lab_time)
        self.lab_time_2 = QtWidgets.QLabel(parent=self.widget1)
        self.lab_time_2.setObjectName("lab_time_2")
        self.horizontalLayout.addWidget(self.lab_time_2)
        self.verticalLayout_2.addLayout(self.horizontalLayout)
        self.gridLayout.addWidget(self.widget1, 3, 0, 1, 2)
        self.sld_video = myVideoSlider(parent=self.widget)
        self.sld_video.setMinimumSize(QtCore.QSize(410, 0))
        self.sld_video.setMaximumSize(QtCore.QSize(16777215, 20))
        self.sld_video.setMaximum(100)
        self.sld_video.setOrientation(QtCore.Qt.Orientation.Horizontal)
        self.sld_video.setObjectName("sld_video")
        self.gridLayout.addWidget(self.sld_video, 2, 0, 1, 1)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.ok.setText(_translate("Dialog", "确定"))
        self.cancel.setText(_translate("Dialog", "取消"))
        self.btn_play.setText(_translate("Dialog", "播放/暂停"))
        self.lab_video.setText(_translate("Dialog", " 0%"))
        self.lab_time.setText(_translate("Dialog", "00:00:00.000"))
        self.lab_time_2.setText(_translate("Dialog", "00:00:00.000"))
from my_QGraphicsView import CustomGraphicsView, myVideoSlider


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec())
