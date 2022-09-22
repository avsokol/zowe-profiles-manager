from PySide6 import QtCore, QtWidgets
from PySide6.QtGui import QStandardItemModel, QStandardItem, QValidator, QCursor, Qt
from PySide6.QtWidgets import QDialog, QDialogButtonBox, QApplication, QMessageBox
from inc.constants import Create_Profile_Title, Edit_Profile_Title, UPDATE_PROFILE, CREATE_PROFILE, SET_DEFAULT_PROFILE
from lib.decorators.wait_cursor import WaitCursor
from lib.exceptions.unexpected_answer_exception import UnexpectedAnswerException
from lib.validators.qaccount_validator import QDsNameValidator
from lib.validators.qds_name_validator import QProfileNameValidator
from lib.validators.qport_validator import QPortValidator
from lib.zowe_cmds import execute_zowe_command
from qt_ui.tso_widget_profile import UiTsoProfileDialog
from qt_wdg.common_widget import CommonWidget
import re


class TsoProfileDialog(QDialog, UiTsoProfileDialog, CommonWidget):

    DEFAULT_REGION_SIZE = 4096

    MIN_REGION_SIZE = 0
    MAX_REGION_SIZE = 2096128

    DEFAULT_LOGON = "IZUFPROC"

    logon_regex = re.compile('(^@|#|$|[A-Z]+[A-Z0-9]*$){1,8}')
    account_regex = re.compile('^@|#|$|[A-Z]{1}[A-Z0-9]{0,6}$')

    DEFAULT_ROWS = 24
    DEFAULT_COLS = 80
    DEFAULT_CP = "037 English-US"
    DEFAULT_CHAR_SET = "697"

    CODE_PAGES = [
        "037 English-US",
        "273 Austria, Germany",
        "277 Denmark, Norway",
        "278 Sweden, Finland",
        "280 Italy",
        "285 United Kingdom",
        "500 International",
        "284 Spain",
        "297 France",
        "275 Portugal, Brazil",
        "437 Personal Computer",
        "1140 English-US",
        "1141 Austria, Germany",
        "1142 Denmark, Norway",
        "1143 Sweden, Finland",
        "1144 Italy",
        "1145 Spain",
        "1146 United Kingdom",
        "1147 France",
        "1148 International",
        "037C English-US C/370",
        "924 Multinational ISO Euro",
        "1047 Latin 1/Open Systems",
        "870 Poland",
        "875 Greece",
        "1025 Russia",
        "424 Hebrew",
        "871 Iceland"
    ]

    CHAR_SETS = [
        "697",
        "235",
        "941",
        "1176",
        "959",
        "923",
        "960",
        "1150",
        "1126",
        "1326",
        "1353",
        "695",
        "1375",
        "1371",
        "1357",
    ]

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
        self.regionEdit.setToolTip("Region size can be between {0} and {1}".format(
            self.MIN_REGION_SIZE,
            self.MAX_REGION_SIZE)
        )

        self.upperCaseModificators = [self.accountEdit, self.logonEdit]

        profile_name_validator = QProfileNameValidator(self.profileEdit)
        self.profileEdit.setValidator(profile_name_validator)

        account_validator = QDsNameValidator(name_type="account", parent=self.accountEdit)
        self.accountEdit.setValidator(account_validator)

        region_size_validator = QPortValidator(
            self.regionEdit,
            bottom=self.MIN_REGION_SIZE,
            top=self.MAX_REGION_SIZE
        )
        self.regionEdit.setValidator(region_size_validator)

        logon_validator = QDsNameValidator(parent=self.logonEdit)
        self.logonEdit.setValidator(logon_validator)

        self.validators = {
            self.profileEdit: self.check_profile_name,
            self.accountEdit: self.check_account_name,
            self.regionEdit: self.check_region_size_param
        }

        self.set_signals()

        self.modelCodePage = QStandardItemModel(self.codePageComboBox)
        for code_page in self.CODE_PAGES:
            self.modelCodePage.appendRow(QStandardItem(code_page))

        self.codePageComboBox.setModel(self.modelCodePage)

        self.charSetModel = QStandardItemModel(self.charsetComboBox)
        for char_set in self.CHAR_SETS:
            self.charSetModel.appendRow(QStandardItem(char_set))

        self.charsetComboBox.setModel(self.charSetModel)

        if self.mode == self.ADD_MODE:
            self.setWindowTitle(Create_Profile_Title.format(self.profile_type.upper()))

        elif self.mode == self.EDIT_MODE:
            self.setWindowTitle(Edit_Profile_Title.format(self.profile_type.upper()))

        if self.mode != self.ADD_MODE:
            self.fill_profile_parameters()
            self.buttonBox.button(QtWidgets.QDialogButtonBox.Ok).setEnabled(False)

        self.show()

    def set_signals(self):
        self.connect(self.buttonBox, QtCore.SIGNAL("accepted()"), self, QtCore.SLOT("accept()"))
        self.connect(self.buttonBox, QtCore.SIGNAL("rejected()"), self, QtCore.SLOT("reject()"))
        self.buttonBox.button(QDialogButtonBox.Reset).clicked.connect(self.reset_form)

        self.profileEdit.textChanged.connect(self.check_input_params_with_validation)
        self.accountEdit.textChanged.connect(self.check_input_params_with_validation)
        self.regionEdit.textChanged.connect(self.check_input_params_with_validation)
        self.logonEdit.textChanged.connect(self.check_input_params_with_validation)
        self.charsetComboBox.currentIndexChanged.connect(self.check_input_params_with_validation)
        self.codePageComboBox.currentIndexChanged.connect(self.check_input_params_with_validation)
        self.columnSpinBox.valueChanged.connect(self.check_input_params_with_validation)
        self.rowSpinBox.valueChanged.connect(self.check_input_params_with_validation)

    def reset_form(self):
        print("Reset")
        self.regionEdit.setText(str(self.DEFAULT_REGION_SIZE))
        self.logonEdit.setText(self.DEFAULT_LOGON)

        self.codePageComboBox.setCurrentIndex(self.CODE_PAGES.index(self.DEFAULT_CP))
        self.charsetComboBox.setCurrentIndex(self.CHAR_SETS.index(self.DEFAULT_CHAR_SET))

        self.rowSpinBox.setValue(self.DEFAULT_ROWS)
        self.columnSpinBox.setValue(self.DEFAULT_COLS)

    def check_empty_params(self):
        account = self.accountEdit.text().strip()
        region_size = self.regionEdit.text().strip()
        logon_proc = self.logonEdit.text().strip()

        params = [account, region_size, logon_proc]
        for param in params:
            if param == "":
                self.log_message("Empty parameter")
                self.buttonBox.button(QtWidgets.QDialogButtonBox.Ok).setEnabled(False)
                return False

        self.log_message("All required parameters are filled")
        return True

    def check_input_params_with_validation(self):
        if self.sender() in self.upperCaseModificators:
            self.sender().setText(self.sender().text().upper())

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

    def check_profile_name(self, sender):
        self.log_message("Account value: '{0}'".format(sender.text()))
        profile_name_validator = QProfileNameValidator(self.profileEdit)

        dialog_state = profile_name_validator.validate(sender.text(), 0)
        if dialog_state == QValidator.Acceptable:
            button_state = True

        elif dialog_state == QValidator.Intermediate:
            button_state = False

        else:
            button_state = False

        return dialog_state, button_state

    def check_account_name(self, sender):
        self.log_message("Account value: '{0}'".format(sender.text()))
        account_validator = QDsNameValidator(name_type="account", parent=self.accountEdit)

        dialog_state = account_validator.validate(sender.text(), 0)
        if dialog_state == QValidator.Acceptable:
            button_state = True

        elif dialog_state == QValidator.Intermediate:
            button_state = False

        else:
            button_state = False

        return dialog_state, button_state

    def check_region_size_param(self, sender):
        self.log_message("Region Size value: '{0}'".format(sender.text()))
        region_size_validator = QPortValidator(
            sender,
            bottom=self.MIN_REGION_SIZE,
            top=self.MAX_REGION_SIZE
        )

        dialog_state = region_size_validator.validate(sender.text(), 0)
        if dialog_state == QValidator.Acceptable:
            button_state = True

        elif dialog_state == QValidator.Intermediate:
            button_state = False

        else:
            button_state = False

        return dialog_state, button_state

    def run_create_profile(self):
        self.log_message("Create tso profile")
        profile_name = self.profileEdit.text().strip()
        set_default = self.setDefault.isChecked()
        account = self.accountEdit.text().strip()
        region_size = int(self.regionEdit.text().strip())
        logon_proc = self.logonEdit.text().strip()
        code_page = self.codePageComboBox.currentText()
        code_page = code_page.split()[0]
        char_set = self.charsetComboBox.currentText()
        rows = self.rowSpinBox.value()
        columns = self.columnSpinBox.value()

        QApplication.setOverrideCursor(QCursor(Qt.WaitCursor))
        try:
            execute_zowe_command(
                CREATE_PROFILE,
                profile_type=self.profile_type,
                profile_name=profile_name,
                account=account,
                regionSize=region_size,
                logonProcedure=logon_proc,
                codePage=code_page,
                characterSet=char_set,
                rows=rows,
                columns=columns
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
                        account=account,
                        regionSize=region_size,
                        logonProcedure=logon_proc,
                        codePage=code_page,
                        characterSet=char_set,
                        rows=rows,
                        columns=columns,
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
        profile_name = self.profileEdit.text().strip()
        account = self.accountEdit.text().strip()
        region_size = int(self.regionEdit.text().strip())
        logon_proc = self.logonEdit.text().strip()
        code_page = self.codePageComboBox.currentText()
        code_page = code_page.split()[0]
        char_set = self.charsetComboBox.currentText()
        rows = self.rowSpinBox.value()
        columns = self.columnSpinBox.value()

        kwargs = dict()

        if account != self.profiles[profile_name]["account"]:
            kwargs["account"] = account

        if region_size != self.profiles[profile_name]["regionSize"]:
            kwargs["regionSize"] = region_size

        if logon_proc != self.profiles[profile_name]["logonProcedure"]:
            kwargs["logonProcedure"] = logon_proc

        if code_page != self.profiles[profile_name]["codePage"]:
            kwargs["codePage"] = code_page

        if char_set != self.profiles[profile_name]["characterSet"]:
            kwargs["characterSet"] = char_set

        if rows != self.profiles[profile_name]["rows"]:
            kwargs["rows"] = rows

        if columns != self.profiles[profile_name]["columns"]:
            kwargs["columns"] = columns

        return kwargs, len(kwargs) > 0

    @WaitCursor()
    def run_edit_profile(self):
        self.log_message("Edit tso profile")

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
        profile_name = self.profile_names[0]
        account_name = self.profiles[profile_name]["account"]
        region_size = self.profiles[profile_name]["regionSize"]
        logon_proc = self.profiles[profile_name]["logonProcedure"]
        code_page = self.profiles[profile_name]["codePage"]
        char_set = self.profiles[profile_name]["characterSet"]
        rows = self.profiles[profile_name]["rows"]
        columns = self.profiles[profile_name]["columns"]

        self.profileEdit.setText(profile_name)
        self.profileEdit.setEnabled(False)

        self.accountEdit.setText(account_name)
        self.regionEdit.setText(str(region_size))
        self.logonEdit.setText(logon_proc)

        if self.mode != self.ADD_MODE:
            self.setDefault.setEnabled(False)

        for cp in self.CODE_PAGES:
            if code_page == cp.split()[0]:
                self.codePageComboBox.setCurrentIndex(self.CODE_PAGES.index(cp))

        self.charsetComboBox.setCurrentIndex(self.CHAR_SETS.index(char_set))

        self.rowSpinBox.setValue(rows)
        self.columnSpinBox.setValue(columns)
