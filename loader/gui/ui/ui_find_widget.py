# Form implementation generated from reading ui file 'd:\python\youtube-loader\src\ui\FindWidget.ui'
#
# Created by: PyQt6 UI code generator 6.3.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_FindWidget(object):
    def setupUi(self, FindWidget):
        FindWidget.setObjectName("FindWidget")
        FindWidget.resize(500, 260)
        FindWidget.setMinimumSize(QtCore.QSize(500, 260))
        FindWidget.setMaximumSize(QtCore.QSize(500, 260))
        self.verticalLayout = QtWidgets.QVBoxLayout(FindWidget)
        self.verticalLayout.setObjectName("verticalLayout")
        spacerItem = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Fixed)
        self.verticalLayout.addItem(spacerItem)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setContentsMargins(-1, -1, -1, 20)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.logo = QtWidgets.QLabel(FindWidget)
        self.logo.setMaximumSize(QtCore.QSize(160, 56))
        self.logo.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        self.logo.setText("")
        self.logo.setPixmap(QtGui.QPixmap("src/img/youtube_logo.png"))
        self.logo.setScaledContents(True)
        self.logo.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.logo.setObjectName("logo")
        self.horizontalLayout_2.addWidget(self.logo)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.url = QtWidgets.QLineEdit(FindWidget)
        self.url.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeading|QtCore.Qt.AlignmentFlag.AlignLeft|QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.url.setObjectName("url")
        self.verticalLayout.addWidget(self.url)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setContentsMargins(-1, 8, -1, -1)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.findButton = QtWidgets.QPushButton(FindWidget)
        self.findButton.setMinimumSize(QtCore.QSize(70, 40))
        self.findButton.setMaximumSize(QtCore.QSize(70, 40))
        self.findButton.setLayoutDirection(QtCore.Qt.LayoutDirection.RightToLeft)
        self.findButton.setObjectName("findButton")
        self.horizontalLayout.addWidget(self.findButton)
        self.verticalLayout.addLayout(self.horizontalLayout)
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Expanding)
        self.verticalLayout.addItem(spacerItem1)

        self.retranslateUi(FindWidget)
        QtCore.QMetaObject.connectSlotsByName(FindWidget)

    def retranslateUi(self, FindWidget):
        _translate = QtCore.QCoreApplication.translate
        FindWidget.setWindowTitle(_translate("FindWidget", "Form"))
        self.url.setPlaceholderText(_translate("FindWidget", "https://www.youtube.com/watch?v="))
        self.findButton.setText(_translate("FindWidget", "Поиск"))
