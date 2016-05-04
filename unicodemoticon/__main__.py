#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import sys

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QStyle

try:
    import qdarkstyle  # https://github.com/ColinDuquesnoy/QDarkStyleSheet
except ImportError:    # sudo pip3 install qdarkstyle
    qdarkstyle = None  # 100% optional

# if this script is executed directly: make relative imports work
if not __package__:
    from pathlib import Path
    parent_dir = Path(__file__).absolute().parent
    sys.path.insert(0, str(parent_dir))
    import unicodemoticon  # noqa
    __package__ = str("unicodemoticon")

from . import TabWidget
from .utils import (make_logger, make_root_check_and_encoding_debug,
                    make_post_execution_message,
                    set_process_name_and_cpu_priority, make_config)


def main(args=sys.argv):
    make_logger("unicodemoticon")
    make_root_check_and_encoding_debug()
    set_process_name_and_cpu_priority("unicodemoticon")
    make_config("unicodemoticon")

    # TODO: single instance
    app = QApplication(args)
    app.setApplicationName("unicodemoticon")
    app.setOrganizationName("unicodemoticon")
    app.setOrganizationDomain("unicodemoticon")
    app.instance().setQuitOnLastWindowClosed(False)  # no quit on dialog quit
    if qdarkstyle:
            app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
    icon = QIcon(app.style().standardPixmap(QStyle.SP_FileIcon))
    app.setWindowIcon(icon)
    win = TabWidget()
    win.show()
    win.hide()
    make_post_execution_message()
    sys.exit(app.exec())


# may be unicodemoticon.__main__
if __name__.endswith("__main__"):
    main()
