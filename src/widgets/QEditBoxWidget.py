# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import QTextEdit
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt


class QEditBoxWidget(QTextEdit):
    def __init__(self, app_obj, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.app_obj = app_obj
        self.setMaximumHeight(70)
        self.setFont(QFont('Monospace', 13))

    def keyPressEvent(self, event):
        if event.key() in (Qt.Key_Return, Qt.Key_Enter):
            self.app_obj.send_message()
        else:
            super().keyPressEvent(event)

