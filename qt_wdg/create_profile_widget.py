from PySide6 import QtCore, QtWidgets
from PySide6.QtGui import QCursor, Qt, QValidator
from PySide6.QtWidgets import QDialog, QMessageBox, QApplication
from lib.decorators.wait_cursor import WaitCursor
from lib.exceptions.unexpected_answer_exception import UnexpectedAnswerException
from lib.zowe_cmds import execute_zowe_command, TYPE_SSH, SSH_PORT
from inc.constants import CREATE_PROFILE, SET_DEFAULT_PROFILE, Create_Profile_Title, Edit_Profile_Title, \
    Edit_Profiles_Title, UPDATE_PROFILE
from qt_ui.create_profile import UiCreateProfileDialog
from lib.validators.qport_validator import QPortValidator
from lib.validators.qds_name_validator import QProfileNameValidator
from qt_wdg.common_widget import CommonWidget


class CreateProfile(QDialog, UiCreateProfileDialog, CommonWidget):

    def __init__(self, profile_type, mode=None, debug=False, parent=None, profiles=None, profile_names=None):
        QDialog.__init__(self, parent)
        self.profile_type = profile_type

        CommonWidget.__init__(self, debug=debug, profile_type=self.profile_type)
        self.mode = mode
        if self.mode is None:
            self.mode = self.ADD_MODE

        self.debug = debug

        if mode == self.EDIT_MODE:
            if None in [profiles, profile_names]:
                raise Exception("Incorrect dialog usage. Not all parameters are supplied")

            self.profiles = profiles
            self.profile_names = profile_names

            if len(self.profile_names) > 1:
                self.mode = self.EDIT_MULTIPLE_MODE

        self.setup_ui(self)
        self.buttonBox.button(QtWidgets.QDialogButtonBox.Ok).setEnabled(False)

        self.validators = {
            self.profileName: self.check_profile_name,
            self.hostport: self.check_port_param
        }

        profile_name_validator = QProfileNameValidator(self.profileName)
        self.profileName.setValidator(profile_name_validator)

        if self.mode != self.EDIT_MULTIPLE_MODE:
            port_validator = QPortValidator(self.hostport)
            self.hostport.setValidator(port_validator)

            self.hostport.setToolTip(
                "Port for {2} in range: {0}-{1}".format(
                    port_validator.get_bottom(), port_validator.get_top(), self.profile_type.upper()
                )
            )

        self.set_signals()
        self.set_ssh_port()

        if self.mode == self.ADD_MODE:
            self.setWindowTitle(Create_Profile_Title.format(self.profile_type.upper()))

        elif self.mode == self.EDIT_MODE:
            self.setWindowTitle(Edit_Profile_Title.format(self.profile_type.upper()))

        elif self.mode == self.EDIT_MULTIPLE_MODE:
            self.setWindowTitle(Edit_Profiles_Title.format(self.profile_type.upper()))

        else:
            raise Exception("Unsupported dialog mode")

        if self.mode != self.ADD_MODE:
            self.fill_profile_parameters()
            self.buttonBox.button(QtWidgets.QDialogButtonBox.Ok).setEnabled(False)

        self.show()
        self.setMinimumWidth(self.width())
        self.setMinimumHeight(self.height())
        self.setMaximumWidth(self.width())
        self.setMaximumHeight(self.height())

    def set_signals(self):
        self.connect(self.buttonBox, QtCore.SIGNAL("accepted()"), self, QtCore.SLOT("accept()"))
        self.connect(self.buttonBox, QtCore.SIGNAL("rejected()"), self, QtCore.SLOT("reject()"))
        self.profileName.textChanged.connect(self.check_input_params_with_validation)
        self.hostname.textChanged.connect(self.check_input_params_with_validation)
        self.hostport.textChanged.connect(self.check_input_params_with_validation)
        self.username.textChanged.connect(self.check_input_params_with_validation)
        self.password.textChanged.connect(self.check_input_params_with_validation)
        self.acceptSelfSigned.stateChanged.connect(self.check_input_params_with_validation)

    def check_input_params_with_validation(self):
        dialog_state, button_state = None, False

        for validator in self.validators:
            dialog_state, button_state = self.validators[validator](validator)

            if dialog_state != QValidator.Acceptable:
                break

        if dialog_state == QValidator.Acceptable:
            button_state = self.check_empty_params()

        if self.mode != self.ADD_MODE and button_state:
            kwargs, button_state = self.params_are_modified()

        self.buttonBox.button(QtWidgets.QDialogButtonBox.Ok).setEnabled(button_state)

    def check_empty_params(self):
        profile_name = self.profileName.text().strip()
        hostname = self.hostname.text().strip()
        port = self.hostport.text().strip()
        username = self.username.text().strip()
        password = self.password.text()

        if self.mode == self.ADD_MODE:
            params = [profile_name, hostname, port, username, password]

        elif self.mode == self.EDIT_MODE:
            params = [hostname, port, username, password]

        elif self.mode == self.EDIT_MULTIPLE_MODE:
            params = [username, password]

        else:
            raise Exception("Unsupported dialog mode")

        for param in params:
            if param == "":
                self.log_message("Empty parameter")
                return False

        self.log_message("All required parameters are filled")
        return True

    def check_profile_name(self, sender):
        self.log_message("Account value: '{0}'".format(sender.text()))
        profile_name_validator = QProfileNameValidator(self.profileName)

        dialog_state = profile_name_validator.validate(sender.text(), 0)
        if dialog_state == QValidator.Acceptable:
            button_state = True

        elif dialog_state == QValidator.Intermediate:
            button_state = False

        else:
            button_state = False

        return dialog_state, button_state

    def check_port_param(self, sender):
        if self.mode == self.EDIT_MULTIPLE_MODE:
            dialog_state = QValidator.Acceptable
            button_state = False

        else:
            port_validator = QPortValidator(sender)

            self.log_message("Port value: '{0}'".format(sender.text()))

            dialog_state = port_validator.validate(sender.text(), 0)
            if dialog_state == QValidator.Acceptable:
                button_state = True

            elif dialog_state == QValidator.Intermediate:
                button_state = False

            else:
                button_state = False

        return dialog_state, button_state

    def run_create_profile(self):
        self.log_message("Create zowe {0} profile".format(self.profile_type))

        profile_name = self.profileName.text().strip()
        set_default = self.setDefaultProfile.isChecked()
        hostname = self.hostname.text().strip()
        port = self.hostport.text().strip()
        username = self.username.text().strip()
        password = self.password.text()
        reject_unauthorised = not self.acceptSelfSigned.isChecked()

        QApplication.setOverrideCursor(QCursor(Qt.WaitCursor))

        try:
            execute_zowe_command(
                CREATE_PROFILE,
                profile_type=self.profile_type,
                profile_name=profile_name,
                host=hostname,
                port=port,
                username=username,
                password=password,
                reject_unauthorised=reject_unauthorised,
                overwrite=False
            )
            if set_default:
                execute_zowe_command(
                    SET_DEFAULT_PROFILE,
                    profile_type=self.profile_type,
                    profile_name=profile_name
                )

            QApplication.restoreOverrideCursor()

        except Exception as e:
            QApplication.restoreOverrideCursor()

            out = e.args[0]
            if self.is_profile_exist(profile_name, out):
                answer = self.yes_no_msg_box(profile_name)

                if answer == QMessageBox.Yes:
                    self.log_message("Overwrite requested")
                    QApplication.setOverrideCursor(QCursor(Qt.WaitCursor))
                    code, out = execute_zowe_command(
                        CREATE_PROFILE,
                        profile_type=self.profile_type,
                        profile_name=profile_name,
                        host=hostname,
                        port=port,
                        username=username,
                        password=password,
                        reject_unauthorised=reject_unauthorised,
                        overwrite=True
                    )
                    if code == 0 and set_default:
                        execute_zowe_command(
                            SET_DEFAULT_PROFILE,
                            profile_type=self.profile_type,
                            profile_name=profile_name
                        )

                    QApplication.restoreOverrideCursor()

                elif answer == QMessageBox.No:
                    self.log_message("No overwrite")
                    return

                else:
                    raise UnexpectedAnswerException

            else:
                raise

        QDialog.accept(self)

    def params_are_modified(self):
        profile_name = self.profileName.text().strip()
        hostname = self.hostname.text().strip()
        port = self.hostport.text().strip()
        username = self.username.text().strip()
        password = self.password.text()
        reject_unauthorised = not self.acceptSelfSigned.isChecked()

        kwargs = dict()

        if self.mode != self.EDIT_MULTIPLE_MODE:
            if hostname != self.profiles[profile_name]["host"]:
                kwargs["host"] = hostname

            if int(port) != int(self.profiles[profile_name]["port"]):
                kwargs["port"] = port

            if username != self.profiles[profile_name]["user"]:
                kwargs["username"] = username

            if password != self.profiles[profile_name]["password"]:
                kwargs["password"] = password

            if self.profile_type != TYPE_SSH:
                if reject_unauthorised != self.profiles[profile_name]["rejectUnauthorized"]:
                    kwargs["reject_unauthorised"] = reject_unauthorised

        if self.mode == self.EDIT_MULTIPLE_MODE:
            kwargs["username"] = username
            kwargs["password"] = password
            kwargs["reject_unauthorised"] = reject_unauthorised

        return kwargs, len(kwargs) > 0

    @WaitCursor()
    def run_edit_profile(self):
        self.log_message("Edit zowe {0} profile".format(self.profile_type))

        kwargs, status = self.params_are_modified()

        if kwargs:
            for profile_name in self.profile_names:
                execute_zowe_command(
                    UPDATE_PROFILE,
                    profile_type=self.profile_type,
                    profile_name=profile_name,
                    **kwargs
                )

        QDialog.accept(self)

    def accept(self):
        if self.mode == self.ADD_MODE:
            return self.run_create_profile()

        else:
            return self.run_edit_profile()

    def fill_profile_parameters(self):
        if self.mode == self.EDIT_MODE:
            profile_name = self.profile_names[0]
            self.profileName.setText(profile_name)
            self.profileName.setEnabled(False)
            self.setDefaultProfile.setEnabled(False)
            self.hostname.setText(self.profiles[profile_name]["host"])
            self.hostport.setText(str(self.profiles[profile_name]["port"]))
            self.hostport.setEnabled(True)
            if self.profile_type == TYPE_SSH:
                self.hostport.setEnabled(False)

            self.username.setText(self.profiles[profile_name]["user"])
            self.password.setText(self.profiles[profile_name]["password"])
            if self.profile_type == TYPE_SSH:
                self.acceptSelfSigned.setEnabled(False)

            else:
                reject_unauthorised = self.profiles[profile_name]["rejectUnauthorized"]
                self.acceptSelfSigned.setEnabled(True)
                self.acceptSelfSigned.setChecked(not reject_unauthorised)

        elif self.mode == self.EDIT_MULTIPLE_MODE:
            self.profileName.setText(", ".join(self.profile_names))
            self.profileName.setEnabled(False)
            self.setDefaultProfile.setEnabled(False)
            self.hostname.setText("")
            self.hostname.setEnabled(False)
            self.hostport.setText("")
            self.hostport.setEnabled(False)

        else:
            raise Exception("Unsupported dialog mode")

    def set_ssh_port(self):
        self.hostport.setEnabled(True)
        self.acceptSelfSigned.setEnabled(True)
        if self.profile_type == TYPE_SSH:
            self.hostport.setText(str(SSH_PORT))
            self.acceptSelfSigned.setEnabled(False)
            self.hostport.setEnabled(False)
