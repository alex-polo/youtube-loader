# Form implementation generated from reading ui file 'd:\python\youtube-loader\src\ui\LoadWidget.ui'
#
# Created by: PyQt6 UI code generator 6.3.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtWidgets
from PyQt6.QtGui import QMovie


class Ui_LoadScreen(object):
    def setupUi(self, LoadScreen):
        LoadScreen.setObjectName("LoadScreen")
        LoadScreen.resize(225, 150)
        self.verticalLayout = QtWidgets.QVBoxLayout(LoadScreen)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtWidgets.QLabel(LoadScreen)
        self.label.setMaximumSize(QtCore.QSize(225, 150))
        self.label.setText("")
        self.label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.movie = QMovie("src/img/load.gif")
        self.movie.setScaledSize(QtCore.QSize(225, 150))
        self.label.setMovie(self.movie)
        self.movie.start()
        self.retranslateUi(LoadScreen)
        QtCore.QMetaObject.connectSlotsByName(LoadScreen)

    def retranslateUi(self, LoadScreen):
        _translate = QtCore.QCoreApplication.translate
        LoadScreen.setWindowTitle(_translate("LoadScreen", "Form"))
