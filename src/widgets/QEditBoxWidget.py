# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import QTextEdit
from PyQt5.QtGui import QFont


class QEditBoxWidget(QTextEdit):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setMaximumHeight(70)
        self.setFont(QFont('Monospace', 13))
