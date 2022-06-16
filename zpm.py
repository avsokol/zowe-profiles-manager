import sys
import os
from PySide2 import QtWidgets, QtGui
from lib.zowe_cmds import execute_zowe_command
from inc.constants import TEST
from qt_wdg.about_widget import About
from qt_wdg.no_zowe_dlg import NoZoweDlg
from qt_wdg.window import Window


def main(params):
    app = QtWidgets.QApplication(sys.argv)
    app.setWindowIcon(QtGui.QIcon(os.path.join(os.path.dirname(os.path.realpath(__file__)), "ico/zowe.xpm")))

    if len(params) == 1 and params[0] == "--about":
        about = About()
        sys.exit(about.exec_())

    elif len(params) == 1 and params[0] == "--version":
        print("Zowe ZOSMF Profiles manager v.1.0")
        exit(0)

    else:
        debug = len(params) == 1 and params[0] == "--debug"

        try:
            execute_zowe_command(TEST)

        except FileNotFoundError as f:
            dlg = NoZoweDlg(f.args[1])
            dlg.show_error_msg_box()

        except Exception:
            raise

        window = Window(debug=debug)
        sys.exit(app.exec_())


if __name__ == "__main__":
    main(sys.argv[1:])
