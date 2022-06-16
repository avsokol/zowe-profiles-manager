import os
from PySide2 import QtCore, QtGui
from PySide2.QtCore import SIGNAL
from PySide2.QtGui import QStandardItemModel, QStandardItem, Qt, QCursor, QFont
from PySide2.QtWidgets import QMainWindow, QApplication, QMessageBox, QMenu
from lib.decorators.wait_cursor import WaitCursor
from lib.exceptions.zoe_cmd_fail_exception import ZoweCmdFailException
from lib.zowe_cmds import execute_zowe_command, ZOWE_ERROR_RESPONSES, get_profiles_from_content, \
    TYPE_SSH, TYPE_ZOSMF, TYPE_TSO
from inc.constants import REFRESH_PROFILES, DELETE_PROFILE, SET_DEFAULT_PROFILE, Application_Title
from qt_wdg.about_widget import About
from qt_wdg.common_widget import CommonWidget
from qt_wdg.create_profile_widget import CreateProfile
from qt_ui.wlayout import UiMainWindow
import re
from qt_wdg.error_msg_box import ErrMsgBox
from qt_wdg.tso_profile_widget import TsoProfileDialog


class Window(QMainWindow, UiMainWindow, CommonWidget):

    def __init__(self, debug=False, parent=None):
        QMainWindow.__init__(self, parent)

        self.debug = debug
        self.setup_ui(self)

        self.zosmf_profiles = dict()
        self.default_profiles = dict()
        self.profile_type = TYPE_ZOSMF
        CommonWidget.__init__(self, debug=self.debug, profile_type=self.profile_type)

        self.setWindowTitle(Application_Title)

        self.set_signals()

        self.models = dict()
        self.models[TYPE_ZOSMF] = QStandardItemModel(self.zosmfProfilesList)
        self.models[TYPE_SSH] = QStandardItemModel(self.sshProfilesList)
        self.models[TYPE_TSO] = QStandardItemModel(self.tsoProfilesList)

        self.zosmfProfilesList.setContextMenuPolicy(Qt.CustomContextMenu)
        self.zosmfProfilesList.customContextMenuRequested.connect(self.profiles_context_menu)

        self.sshProfilesList.setContextMenuPolicy(Qt.CustomContextMenu)
        self.sshProfilesList.customContextMenuRequested.connect(self.profiles_context_menu)

        self.tsoProfilesList.setContextMenuPolicy(Qt.CustomContextMenu)
        self.tsoProfilesList.customContextMenuRequested.connect(self.profiles_context_menu)

        self.tabWidget.currentChanged.connect(self.set_current_profile_type)
        self.show()

        self.update()
        self.repaint()

        self.refresh_profiles_list()

    def set_current_profile_type(self):
        tab_id = self.tabWidget.currentIndex()
        self.profile_type = self.tabWidget.tabText(tab_id).lower()
        self.log_message("Currently handling '{0}' profile type.".format(self.profile_type))
        if self.profile_type not in self.zosmf_profiles:
            self.refresh_profiles_list()

        self.selection_changed()

    def set_signals(self):
        QtCore.QObject.connect(self.createProfile, SIGNAL("clicked()"), self.create_profile)
        QtCore.QObject.connect(self.editProfile, SIGNAL("clicked()"), self.edit_profile)
        QtCore.QObject.connect(self.deleteProfile, SIGNAL("clicked()"), self.delete_profile)
        QtCore.QObject.connect(self.setDefaultProfile, SIGNAL("clicked()"), self.set_default_profile)
        QtCore.QObject.connect(self.refreshProfiles, SIGNAL("clicked()"), self.refresh_profiles_list)

        QtCore.QObject.connect(self.actionAbout, SIGNAL("triggered()"), self.show_about)
        QtCore.QObject.connect(self.actionExit, SIGNAL("triggered()"), self.exit_app)

        QtCore.QObject.connect(self.actionCreateProfile, SIGNAL("triggered()"), self.create_profile)
        QtCore.QObject.connect(self.actionEditProfile, SIGNAL("triggered()"), self.edit_profile)
        QtCore.QObject.connect(self.actionDeleteProfile, SIGNAL("triggered()"), self.delete_profile)
        QtCore.QObject.connect(self.actionSetDefaultProfile, SIGNAL("triggered()"), self.set_default_profile)
        QtCore.QObject.connect(self.actionRefreshProfiles, SIGNAL("triggered()"), self.refresh_profiles_list)

    def profiles_context_menu(self, position):

        selected_indexes = self.get_current_selected_indexes()

        selected_indexes_num = len(selected_indexes)

        menu = QMenu()

        if selected_indexes_num == 0:
            create_item = menu.addAction(self.tr("Create Profile"))
            create_pict = os.path.join(os.path.dirname(os.path.realpath(__file__)), "../ico/add2.png")
            create_icon = QtGui.QIcon(create_pict)
            create_item.setIcon(create_icon)
            QtCore.QObject.connect(create_item, SIGNAL("triggered()"), self.create_profile)

            refresh_item = menu.addAction(self.tr("Refresh"))
            refresh_pict = os.path.join(os.path.dirname(os.path.realpath(__file__)), "../ico/refresh.png")
            refresh_icon = QtGui.QIcon(refresh_pict)
            refresh_item.setIcon(refresh_icon)
            QtCore.QObject.connect(refresh_item, SIGNAL("triggered()"), self.refresh_profiles_list)

        elif selected_indexes_num == 1:
            edit_item = menu.addAction(self.tr("Edit Profile"))
            edit_pict = os.path.join(os.path.dirname(os.path.realpath(__file__)), "../ico/edit.png")
            edit_icon = QtGui.QIcon(edit_pict)
            edit_item.setIcon(edit_icon)
            QtCore.QObject.connect(edit_item, SIGNAL("triggered()"), self.edit_profile)

            delete_item = menu.addAction(self.tr("Delete Profile"))
            delete_pict = os.path.join(os.path.dirname(os.path.realpath(__file__)), "../ico/delete2.png")
            delete_icon = QtGui.QIcon(delete_pict)
            delete_item.setIcon(delete_icon)
            QtCore.QObject.connect(delete_item, SIGNAL("triggered()"), self.delete_profile)

            profile = selected_indexes[0]
            profile_name = self.models[self.profile_type].item(profile.row()).text().strip()

            if profile_name != self.default_profiles[self.profile_type]:
                default_item = menu.addAction(self.tr("Set Default"))
                default_pict = os.path.join(os.path.dirname(os.path.realpath(__file__)), "../ico/check2.png")
                default_icon = QtGui.QIcon(default_pict)
                default_item.setIcon(default_icon)
                QtCore.QObject.connect(default_item, SIGNAL("triggered()"), self.set_default_profile)

        else:
            edit_item = menu.addAction(self.tr("Edit Profile"))
            edit_pict = os.path.join(os.path.dirname(os.path.realpath(__file__)), "../ico/edit.png")
            edit_icon = QtGui.QIcon(edit_pict)
            edit_item.setIcon(edit_icon)
            QtCore.QObject.connect(edit_item, SIGNAL("triggered()"), self.edit_profile)

            delete_item = menu.addAction(self.tr("Delete Profile"))
            delete_pict = os.path.join(os.path.dirname(os.path.realpath(__file__)), "../ico/delete2.png")
            delete_icon = QtGui.QIcon(delete_pict)
            delete_item.setIcon(delete_icon)
            QtCore.QObject.connect(delete_item, SIGNAL("triggered()"), self.delete_profile)

        if self.profile_type == TYPE_ZOSMF:
            menu.exec_(self.zosmfProfilesList.viewport().mapToGlobal(position))

        elif self.profile_type == TYPE_SSH:
            menu.exec_(self.sshProfilesList.viewport().mapToGlobal(position))

        elif self.profile_type == TYPE_TSO:
            menu.exec_(self.tsoProfilesList.viewport().mapToGlobal(position))

        else:
            raise Exception("Unsupported ZOWE profile type: '{0}'".format(self.profile_type))

    def exit_app(self):
        self.log_message("Exit app!")
        QApplication.quit()

    def show_about(self):
        self.log_message("Show About dialog")
        about = About()
        about.exec_()

    def create_profile(self):
        QApplication.setOverrideCursor(QCursor(Qt.WaitCursor))
        self.disable_buttons()
        self.repaint()

        if self.profile_type != TYPE_TSO:
            widget = CreateProfile(self.profile_type, debug=self.debug, parent=self)

        else:
            widget = TsoProfileDialog(self.profile_type, debug=self.debug, parent=self)

        QApplication.restoreOverrideCursor()

        dialog_result = widget.exec_()
        if dialog_result:
            self.refresh_profiles_list()

        else:
            self.update_buttons_state()

    @WaitCursor()
    def set_default_profile(self):
        self.log_message("set default profile")
        self.disable_buttons()
        self.update()
        self.repaint()
        profile_indexes = self.get_current_selected_indexes()
        if len(profile_indexes) > 1:
            return

        profile = profile_indexes[0]
        profile_name = self.models[self.profile_type].item(profile.row()).text().strip()

        if profile_name == self.default_profiles[self.profile_type]:
            self.update_buttons_state()
            return

        self.log_message("profile_name: '{0}'".format(profile_name))

        code, out = execute_zowe_command(
            SET_DEFAULT_PROFILE,
            profile_type=self.profile_type,
            profile_name=profile_name
        )
        if code == 0:
            self.refresh_profiles_list()

        else:
            self.update_buttons_state()

    @staticmethod
    def ok_cancel_msg_box(profile_names):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Question)
        msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        msg.setDefaultButton(QMessageBox.Cancel)
        msg.setWindowTitle("Are you sure?")
        if len(profile_names) == 1:
            text = "Do you really want to delete the following profile: '{0}'?".format(", ".join(profile_names))

        else:
            text = "Do you really want to delete the following profiles: '{0}'?".format(", ".join(profile_names))

        msg.setText(text)
        msg.show()
        return msg.exec_()

    @WaitCursor()
    def run_delete_profiles(self, indexes, profile_indexes):
        indexes = sorted(indexes)[::-1]
        for index in indexes:
            for profile in profile_indexes:
                if profile.row() == index:
                    profile_name = self.models[self.profile_type].item(profile.row()).text().strip()
                    orig_profile_name = profile_name
                    self.log_message("profile_name: '{0}'".format(profile_name))

                    try:
                        code, out = execute_zowe_command(
                            DELETE_PROFILE,
                            profile_type=self.profile_type,
                            profile_name=profile_name
                        )
                        if code == 0:
                            self.models[self.profile_type].removeRow(profile.row())
                            del(self.zosmf_profiles[self.profile_type][profile_name])

                        break

                    except ZoweCmdFailException as z:
                        for line in "\n".join(z.args).split("\n"):
                            if re.search(
                                    ZOWE_ERROR_RESPONSES[DELETE_PROFILE].format(self.profile_type, profile_name), line
                            ):
                                try:
                                    code, out = execute_zowe_command(
                                        DELETE_PROFILE,
                                        profile_type=self.profile_type,
                                        profile_name=orig_profile_name
                                    )
                                    if code == 0:
                                        self.models[self.profile_type].removeRow(profile.row())
                                        return

                                except ZoweCmdFailException:
                                    pass

                                except Exception:
                                    raise

                        QApplication.restoreOverrideCursor()
                        QApplication.processEvents()

                        errmsg = ErrMsgBox("Zowe command failed", "\n".join(z.args))
                        errmsg.show_error_msg_box()

                    except Exception:
                        raise

    def edit_profile(self):
        self.log_message("Edit profile")
        QApplication.setOverrideCursor(QCursor(Qt.WaitCursor))
        self.disable_buttons()
        self.repaint()

        code, output = execute_zowe_command(
            REFRESH_PROFILES,
            profile_type=self.profile_type,
            show_contents=True
        )
        profiles, default_profile = get_profiles_from_content(output)
        self.default_profiles[self.profile_type] = default_profile
        profile_indexes = self.get_current_selected_indexes()

        indexes = list()
        profile_names = list()
        for profile in profile_indexes:
            indexes.append(profile.row())
            profile_name = self.models[self.profile_type].item(profile.row()).text()
            profile_names.append(profile_name)

        self.log_message("indexes: '{0}'".format(indexes))
        self.log_message("profile_indexes: {0}".format(profile_indexes))

        if self.profile_type != TYPE_TSO:
            widget = CreateProfile(
                self.profile_type,
                mode=CreateProfile.EDIT_MODE,
                debug=self.debug,
                parent=self,
                profiles=profiles,
                profile_names=profile_names
            )

        else:
            widget = TsoProfileDialog(
                self.profile_type,
                mode=TsoProfileDialog.EDIT_MODE,
                debug=self.debug,
                parent=self,
                profiles=profiles,
                profile_names=profile_names
            )

        QApplication.restoreOverrideCursor()
        dialog_result = widget.exec_()

        if dialog_result:
            self.refresh_profiles_list()

        else:
            self.update_buttons_state()

    def delete_profile(self):
        self.log_message("delete profile(s)")
        self.disable_buttons()
        self.update()
        self.repaint()

        profile_indexes = self.get_current_selected_indexes()
        self.log_message("indexes: '{0}'".format(profile_indexes))

        indexes = list()
        profile_names = list()
        for profile in profile_indexes:
            indexes.append(profile.row())
            profile_name = self.models[self.profile_type].item(profile.row()).text()
            profile_names.append(profile_name)

        self.log_message("indexes: '{0}'".format(indexes))
        self.log_message("profile_indexes: {0}".format(profile_indexes))

        if self.ok_cancel_msg_box(profile_names) == QMessageBox.Ok:
            self.run_delete_profiles(indexes, profile_indexes)

        else:
            self.update_buttons_state()

    @WaitCursor()
    def refresh_profiles_list(self):
        self.log_message("refresh profiles")
        self.disable_buttons()
        self.update()
        self.repaint()
        code, content = execute_zowe_command(
            REFRESH_PROFILES,
            profile_type=self.profile_type,
            show_contents=True
        )
        if code != 0:
            raise ZoweCmdFailException

        zowe_profiles, default_profile = get_profiles_from_content(content)
        self.default_profiles[self.profile_type] = default_profile

        self.zosmf_profiles[self.profile_type] = dict()
        self.zosmf_profiles[self.profile_type] = zowe_profiles

        self.models[self.profile_type].clear()

        if self.profile_type == TYPE_ZOSMF:
            self.zosmfProfilesList.setModel(self.models[self.profile_type])
            self.zosmfProfilesList.selectionModel().selectionChanged.connect(self.selection_changed)

        elif self.profile_type == TYPE_SSH:
            self.sshProfilesList.setModel(self.models[self.profile_type])
            self.sshProfilesList.selectionModel().selectionChanged.connect(self.selection_changed)

        elif self.profile_type == TYPE_TSO:
            self.tsoProfilesList.setModel(self.models[self.profile_type])
            self.tsoProfilesList.selectionModel().selectionChanged.connect(self.selection_changed)

        else:
            raise Exception("Unsupported ZOWE profile type: '{0}'".format(self.profile_type))

        i = 0
        for zowe_profile in self.zosmf_profiles[self.profile_type]:
            self.models[self.profile_type].appendRow(QStandardItem(zowe_profile))

            if zowe_profile == self.default_profiles[self.profile_type]:
                font = QFont()
                font.setBold(True)
                self.models[self.profile_type].item(i).setFont(font)

            data = self.zosmf_profiles[self.profile_type][zowe_profile]
            if self.profile_type in [TYPE_ZOSMF, TYPE_SSH]:
                message = "profile: '{0}'\nhost: {1}:{2}\nusername: {3}".format(
                    zowe_profile, data["host"], data["port"], data["user"]
                )

            else:
                message = "profile: '{0}'\naccount:'{1}'\nlogon procedure: '{2}'\nregion size: '{3}'".format(
                    zowe_profile, data["account"], data["logonProcedure"], data["regionSize"]
                )

            self.models[self.profile_type].item(i).setToolTip(message)

            i = i + 1

        self.update_buttons_state()

    def get_current_selected_indexes(self):
        if self.profile_type == TYPE_ZOSMF:
            profile_indexes = self.zosmfProfilesList.selectedIndexes()

        elif self.profile_type == TYPE_SSH:
            profile_indexes = self.sshProfilesList.selectedIndexes()

        elif self.profile_type == TYPE_TSO:
            profile_indexes = self.tsoProfilesList.selectedIndexes()

        else:
            raise Exception("Unsupported ZOWE profile type: '{0}'".format(self.profile_type))

        return profile_indexes

    def selection_changed(self):
        self.update_buttons_state()

        selected_indexes = self.get_current_selected_indexes()
        selected_indexes_num = len(selected_indexes)

        if selected_indexes_num == 1:
            profile = selected_indexes[0]
            profile_name = self.models[self.profile_type].item(profile.row()).text().strip()
            data = self.zosmf_profiles[self.profile_type][profile_name]
            if self.profile_type != TYPE_TSO:
                message = "host: {0}:{1}  username: {2}".format(data["host"], data["port"], data["user"])

            else:
                message = "account: '{0}'\nlogon procedure: '{1}'\nregion size: '{2}'".format(
                    data["account"], data["logonProcedure"], data["regionSize"]
                )

            self.statusbar.showMessage(message)

        else:
            self.statusbar.clearMessage()

    def update_buttons_state(self):
        self.log_message("update button state")

        self.createProfile.setEnabled(True)
        self.editProfile.setEnabled(True)
        self.refreshProfiles.setEnabled(True)

        self.setDefaultProfile.setEnabled(False)
        self.actionSetDefaultProfile.setEnabled(False)

        self.actionCreateProfile.setEnabled(True)
        self.actionEditProfile.setEnabled(True)
        self.actionRefreshProfiles.setEnabled(True)

        selected_indexes = self.get_current_selected_indexes()
        selected_indexes_num = len(selected_indexes)
        self.log_message("'{0}' items selected".format(selected_indexes_num))

        if selected_indexes_num == 0:
            self.editProfile.setEnabled(False)
            self.deleteProfile.setEnabled(False)
            self.setDefaultProfile.setEnabled(False)

            self.actionEditProfile.setEnabled(False)
            self.actionDeleteProfile.setEnabled(False)
            self.actionSetDefaultProfile.setEnabled(False)

        elif selected_indexes_num == 1:
            self.editProfile.setEnabled(True)
            self.deleteProfile.setEnabled(True)
            self.setDefaultProfile.setEnabled(True)

            self.actionEditProfile.setEnabled(True)
            self.actionDeleteProfile.setEnabled(True)
            self.actionSetDefaultProfile.setEnabled(True)

            profile = selected_indexes[0]
            profile_name = self.models[self.profile_type].item(profile.row()).text().strip()

            if profile_name == self.default_profiles[self.profile_type]:
                self.setDefaultProfile.setEnabled(False)
                self.actionSetDefaultProfile.setEnabled(False)

        else:
            self.deleteProfile.setEnabled(True)
            self.setDefaultProfile.setEnabled(False)

            self.actionDeleteProfile.setEnabled(True)
            self.actionSetDefaultProfile.setEnabled(False)

        self.repaint()

    def disable_buttons(self):
        self.createProfile.setEnabled(False)
        self.editProfile.setEnabled(False)
        self.deleteProfile.setEnabled(False)
        self.setDefaultProfile.setEnabled(False)
        self.refreshProfiles.setEnabled(False)

        self.actionCreateProfile.setEnabled(False)
        self.actionEditProfile.setEnabled(False)
        self.actionDeleteProfile.setEnabled(False)
        self.actionSetDefaultProfile.setEnabled(False)
        self.actionRefreshProfiles.setEnabled(False)
