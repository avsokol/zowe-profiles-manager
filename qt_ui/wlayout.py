# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'wlayout.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!
import os
from PySide2 import QtCore, QtGui, QtWidgets
from PySide2.QtWidgets import QAbstractItemView, QStatusBar


class UiMainWindow(object):
    def setup_ui(self, main_window):
        main_window.setObjectName("main_window")
        main_window.resize(488, 360)
        self.centralwidget = QtWidgets.QWidget(main_window)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.mainFrame = QtWidgets.QFrame(self.centralwidget)
        self.mainFrame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.mainFrame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.mainFrame.setObjectName("mainFrame")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.mainFrame)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.tabWidget = QtWidgets.QTabWidget(self.mainFrame)
        self.tabWidget.setObjectName("tabWidget")

        self.zosmf = QtWidgets.QWidget()
        self.zosmf.setObjectName("zosmf")

        self.gridLayout_2 = QtWidgets.QGridLayout(self.zosmf)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.zosmfProfilesList = QtWidgets.QListView(self.zosmf)
        self.zosmfProfilesList.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.zosmfProfilesList.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.zosmfProfilesList.setObjectName("zosmfProfilesList")
        self.gridLayout_2.addWidget(self.zosmfProfilesList, 0, 0, 1, 1)
        self.tabWidget.addTab(self.zosmf, "")

        self.tabSSH = QtWidgets.QWidget()
        self.tabSSH.setObjectName("tabSSH")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.tabSSH)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.sshProfilesList = QtWidgets.QListView(self.tabSSH)
        self.sshProfilesList.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.sshProfilesList.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.sshProfilesList.setObjectName("sshProfilesList")
        self.gridLayout_3.addWidget(self.sshProfilesList, 0, 0, 1, 1)
        self.tabWidget.addTab(self.tabSSH, "")

        self.tabTSO = QtWidgets.QWidget()
        self.tabTSO.setObjectName("tabTSO")
        self.gridLayout_4 = QtWidgets.QGridLayout(self.tabTSO)
        self.gridLayout_4.setObjectName("gridLayout_3")
        self.tsoProfilesList = QtWidgets.QListView(self.tabTSO)
        self.tsoProfilesList.setSelectionMode(QAbstractItemView.SingleSelection)
        self.tsoProfilesList.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tsoProfilesList.setObjectName("tsoProfilesList")
        self.gridLayout_4.addWidget(self.tsoProfilesList, 0, 0, 1, 1)
        self.tabWidget.addTab(self.tabTSO, "")

        self.horizontalLayout_2.addWidget(self.tabWidget)
        self.frame = QtWidgets.QFrame(self.mainFrame)
        self.frame.setAutoFillBackground(True)
        self.frame.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame.setFrameShadow(QtWidgets.QFrame.Plain)
        self.frame.setObjectName("frame")
        self.frame.setAutoFillBackground(True)
        self.verticalLayout = QtWidgets.QVBoxLayout(self.frame)
        self.verticalLayout.setObjectName("verticalLayout")
        spacer_item = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacer_item)
        self.createProfile = QtWidgets.QPushButton(self.frame)

        icon1 = QtGui.QIcon()
        icon1.addPixmap(
            QtGui.QPixmap(os.path.join(os.path.dirname(os.path.realpath(__file__)), "../ico/add2.png")),
            QtGui.QIcon.Normal,
            QtGui.QIcon.Off
        )
        self.createProfile.setIcon(icon1)

        self.createProfile.setObjectName("createProfile")
        self.verticalLayout.addWidget(self.createProfile)
        spacer_item1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacer_item1)
        self.editProfile = QtWidgets.QPushButton(self.frame)

        icon2 = QtGui.QIcon()
        icon2.addPixmap(
            QtGui.QPixmap(os.path.join(os.path.dirname(os.path.realpath(__file__)), "../ico/edit.png")),
            QtGui.QIcon.Normal,
            QtGui.QIcon.Off
        )
        self.editProfile.setIcon(icon2)

        self.editProfile.setObjectName("editProfile")
        self.verticalLayout.addWidget(self.editProfile)
        spacer_item2 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacer_item2)
        self.deleteProfile = QtWidgets.QPushButton(self.frame)

        icon3 = QtGui.QIcon()
        icon3.addPixmap(
            QtGui.QPixmap(os.path.join(os.path.dirname(os.path.realpath(__file__)), "../ico/delete2.png")),
            QtGui.QIcon.Normal,
            QtGui.QIcon.Off
        )
        self.deleteProfile.setIcon(icon3)

        self.deleteProfile.setObjectName("deleteProfile")
        self.verticalLayout.addWidget(self.deleteProfile)
        spacer_item3 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacer_item3)
        self.setDefaultProfile = QtWidgets.QPushButton(self.frame)

        icon4 = QtGui.QIcon()
        icon4.addPixmap(
            QtGui.QPixmap(os.path.join(os.path.dirname(os.path.realpath(__file__)), "../ico/check2.png")),
            QtGui.QIcon.Normal,
            QtGui.QIcon.Off
        )
        self.setDefaultProfile.setIcon(icon4)

        self.setDefaultProfile.setObjectName("setDefaultProfile")
        self.verticalLayout.addWidget(self.setDefaultProfile)
        spacer_item4 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacer_item4)
        self.refreshProfiles = QtWidgets.QPushButton(self.frame)

        icon5 = QtGui.QIcon()
        icon5.addPixmap(
            QtGui.QPixmap(os.path.join(os.path.dirname(os.path.realpath(__file__)), "../ico/refresh.png")),
            QtGui.QIcon.Normal,
            QtGui.QIcon.Off
        )
        self.refreshProfiles.setIcon(icon5)

        self.refreshProfiles.setObjectName("refreshProfiles")
        self.verticalLayout.addWidget(self.refreshProfiles)
        self.horizontalLayout_2.addWidget(self.frame)
        self.verticalLayout_2.addWidget(self.mainFrame)

        main_window.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(main_window)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 488, 22))
        self.menubar.setObjectName("menubar")
        self.menuHelp = QtWidgets.QMenu(self.menubar)
        self.menuHelp.setObjectName("menuHelp")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        main_window.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(main_window)
        self.statusbar.setObjectName("statusbar")
        main_window.setStatusBar(self.statusbar)
        self.actionAbout = QtWidgets.QAction(main_window)
        self.actionAbout.setObjectName("actionAbout")

        self.actionAbout = QtWidgets.QAction(main_window)
        about_icon = QtGui.QIcon()
        about_icon.addPixmap(
            QtGui.QPixmap(os.path.join(os.path.dirname(os.path.realpath(__file__)), "../ico/about.png")),
            QtGui.QIcon.Normal,
            QtGui.QIcon.Off
        )
        self.actionAbout.setIcon(about_icon)

        self.actionCreateProfile = QtWidgets.QAction(main_window)
        self.actionCreateProfile.setIcon(icon1)
        self.actionCreateProfile.setObjectName("actionCreateProfile")
        self.actionEditProfile = QtWidgets.QAction(main_window)
        self.actionEditProfile.setIcon(icon2)
        self.actionEditProfile.setObjectName("actionEditProfile")
        self.actionDeleteProfile = QtWidgets.QAction(main_window)
        self.actionDeleteProfile.setIcon(icon3)
        self.actionDeleteProfile.setObjectName("actionDeleteProfile")
        self.actionSetDefaultProfile = QtWidgets.QAction(main_window)
        self.actionSetDefaultProfile.setIcon(icon4)
        self.actionSetDefaultProfile.setObjectName("actionSetDefaultProfile")
        self.actionRefreshProfiles = QtWidgets.QAction(main_window)
        self.actionRefreshProfiles.setIcon(icon5)
        self.actionRefreshProfiles.setObjectName("actionRefreshProfiles")
        self.actionExit = QtWidgets.QAction(main_window)
        self.actionExit.setObjectName("actionExit")
        self.menuHelp.addAction(self.actionAbout)
        self.menuFile.addAction(self.actionCreateProfile)
        self.menuFile.addAction(self.actionEditProfile)
        self.menuFile.addAction(self.actionDeleteProfile)
        self.menuFile.addAction(self.actionSetDefaultProfile)
        self.menuFile.addAction(self.actionRefreshProfiles)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionExit)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())

        self.statusbar = QStatusBar(main_window)
        self.statusbar.setObjectName("statusbar")
        main_window.setStatusBar(self.statusbar)

        self.retranslate_ui(main_window)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(main_window)

    def retranslate_ui(self, main_window):
        _translate = QtCore.QCoreApplication.translate
        main_window.setWindowTitle(_translate("main_window", "main_window"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.zosmf), _translate("main_window", "ZOSMF"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabSSH), _translate("main_window", "SSH"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabTSO), _translate("main_window", "TSO"))
        self.createProfile.setText(_translate("main_window", "Create Profile"))
        self.editProfile.setText(_translate("main_window", "Edit Profile"))
        self.deleteProfile.setText(_translate("main_window", "Delete Profile"))
        self.setDefaultProfile.setText(_translate("main_window", "Set Default"))
        self.refreshProfiles.setText(_translate("main_window", "Refresh"))
        self.menuHelp.setTitle(_translate("main_window", "Help"))
        self.menuFile.setTitle(_translate("main_window", "File"))
        self.actionAbout.setText(_translate("main_window", "About"))
        self.actionCreateProfile.setText(_translate("main_window", "Create Profile"))
        self.actionEditProfile.setText(_translate("main_window", "Edit Profile"))
        self.actionDeleteProfile.setText(_translate("main_window", "Delete Profile"))
        self.actionSetDefaultProfile.setText(_translate("main_window", "Set Default"))
        self.actionRefreshProfiles.setText(_translate("main_window", "Refresh"))
        self.actionExit.setText(_translate("main_window", "Exit"))
