# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'create_profile.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PySide6 import QtCore, QtWidgets


class UiCreateProfileDialog(object):
    def setup_ui(self, create_profile_dialog):
        create_profile_dialog.setObjectName("tso_profile_dialog")
        create_profile_dialog.setWindowModality(QtCore.Qt.ApplicationModal)
        create_profile_dialog.resize(431, 396)
        self.buttonBox = QtWidgets.QDialogButtonBox(create_profile_dialog)
        self.buttonBox.setGeometry(QtCore.QRect(249, 360, 166, 24))
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel | QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.profileGroup = QtWidgets.QGroupBox(create_profile_dialog)
        self.profileGroup.setGeometry(QtCore.QRect(10, 10, 411, 80))
        self.profileGroup.setObjectName("profileGroup")
        self.profileName = QtWidgets.QLineEdit(self.profileGroup)
        self.profileName.setGeometry(QtCore.QRect(54, 42, 191, 23))
        self.profileName.setObjectName("profileName")
        self.nameLabel = QtWidgets.QLabel(self.profileGroup)
        self.nameLabel.setGeometry(QtCore.QRect(10, 44, 36, 16))
        self.nameLabel.setObjectName("nameLabel")
        self.setDefaultProfile = QtWidgets.QCheckBox(self.profileGroup)
        self.setDefaultProfile.setGeometry(QtCore.QRect(280, 43, 109, 21))
        self.setDefaultProfile.setObjectName("setDefaultProfile")
        self.hostGroup = QtWidgets.QGroupBox(create_profile_dialog)
        self.hostGroup.setGeometry(QtCore.QRect(10, 110, 411, 80))
        self.hostGroup.setObjectName("hostGroup")
        self.hostname = QtWidgets.QLineEdit(self.hostGroup)
        self.hostname.setGeometry(QtCore.QRect(77, 41, 180, 23))
        self.hostname.setObjectName("hostname")
        self.hostport = QtWidgets.QLineEdit(self.hostGroup)
        self.hostport.setGeometry(QtCore.QRect(330, 41, 50, 23))
        self.hostport.setObjectName("hostport")
        self.labelHostName = QtWidgets.QLabel(self.hostGroup)
        self.labelHostName.setGeometry(QtCore.QRect(10, 43, 60, 16))
        self.labelHostName.setObjectName("labelHostName")
        self.labelPort = QtWidgets.QLabel(self.hostGroup)
        self.labelPort.setGeometry(QtCore.QRect(299, 43, 25, 16))
        self.labelPort.setObjectName("labelPort")
        self.credentialsGroup = QtWidgets.QGroupBox(create_profile_dialog)
        self.credentialsGroup.setGeometry(QtCore.QRect(10, 210, 411, 131))
        self.credentialsGroup.setObjectName("credentialsGroup")
        self.layoutWidget = QtWidgets.QWidget(self.credentialsGroup)
        self.layoutWidget.setGeometry(QtCore.QRect(10, 40, 389, 25))
        self.layoutWidget.setObjectName("layoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.layoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.usernameLabel = QtWidgets.QLabel(self.layoutWidget)
        self.usernameLabel.setObjectName("usernameLabel")
        self.horizontalLayout.addWidget(self.usernameLabel)
        self.username = QtWidgets.QLineEdit(self.layoutWidget)
        self.username.setObjectName("username")
        self.horizontalLayout.addWidget(self.username)
        self.passwordLabel = QtWidgets.QLabel(self.layoutWidget)
        self.passwordLabel.setObjectName("passwordLabel")
        self.horizontalLayout.addWidget(self.passwordLabel)
        self.password = QtWidgets.QLineEdit(self.layoutWidget)
        self.password.setInputMethodHints(
            QtCore.Qt.ImhHiddenText |
            QtCore.Qt.ImhNoAutoUppercase |
            QtCore.Qt.ImhNoPredictiveText |
            QtCore.Qt.ImhSensitiveData
        )
        self.password.setEchoMode(QtWidgets.QLineEdit.Password)
        self.password.setObjectName("password")
        self.horizontalLayout.addWidget(self.password)
        self.acceptSelfSigned = QtWidgets.QCheckBox(self.credentialsGroup)
        self.acceptSelfSigned.setGeometry(QtCore.QRect(10, 90, 200, 21))
        self.acceptSelfSigned.setObjectName("acceptSelfSigned")

        self.retranslate_ui(create_profile_dialog)
        QtCore.QMetaObject.connectSlotsByName(create_profile_dialog)

    def retranslate_ui(self, create_profile_dialog):
        _translate = QtCore.QCoreApplication.translate
        create_profile_dialog.setWindowTitle(_translate("tso_profile_dialog", "dialog"))
        self.profileGroup.setTitle(_translate("tso_profile_dialog", "Profile"))
        self.profileName.setToolTip(_translate("tso_profile_dialog", "Enter profile name"))
        self.nameLabel.setText(_translate("tso_profile_dialog", "Name"))
        self.setDefaultProfile.setToolTip(_translate(
            "tso_profile_dialog", "Check to set this profile to be default one")
        )
        self.setDefaultProfile.setText(_translate("tso_profile_dialog", "Set as default"))
        self.hostGroup.setTitle(_translate("tso_profile_dialog", "Host"))
        self.hostname.setToolTip(_translate("tso_profile_dialog", "Hostname or IP for ZOSMF"))
        self.hostport.setToolTip(_translate("tso_profile_dialog", "Port for ZOSMF"))
        self.labelHostName.setText(_translate("tso_profile_dialog", "Hostname"))
        self.labelPort.setText(_translate("tso_profile_dialog", "Port"))
        self.credentialsGroup.setTitle(_translate("tso_profile_dialog", "Credentials"))
        self.usernameLabel.setText(_translate("tso_profile_dialog", "Username"))
        self.username.setToolTip(_translate("tso_profile_dialog", "Mainframe username"))
        self.passwordLabel.setText(_translate("tso_profile_dialog", "Password"))
        self.password.setToolTip(_translate("tso_profile_dialog", "Mainframe password"))
        self.acceptSelfSigned.setText(_translate("tso_profile_dialog", "Accept self-signed certificate"))
