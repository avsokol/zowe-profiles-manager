from PySide2.QtWidgets import QMessageBox
from inc.constants import Overwrite_Profile_Template, CREATE_PROFILE
import re

from lib.zowe_cmds import ZOWE_ERROR_RESPONSES


class CommonWidget(object):

    ADD_MODE = "add"
    EDIT_MODE = "edit"
    EDIT_MULTIPLE_MODE = "edit_multi"

    def __init__(self, debug=False, profile_type=None):
        self.debug = debug
        self.profile_type = profile_type

    @staticmethod
    def yes_no_msg_box(profile_name):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Warning)
        msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        msg.setDefaultButton(QMessageBox.No)
        msg.setWindowTitle("Warning")
        msg.setText(Overwrite_Profile_Template.format(profile_name))
        msg.show()
        return msg.exec_()

    def log_message(self, msg):
        if self.debug:
            print(msg)

    def is_profile_exist(self, profile_name, output):
        self.log_message("output: '{0}': '{1}'".format(output, type(output)))
        for line in output.split("\n"):
            if re.match(ZOWE_ERROR_RESPONSES[CREATE_PROFILE].format(self.profile_type, profile_name), line):
                return True

        return False
