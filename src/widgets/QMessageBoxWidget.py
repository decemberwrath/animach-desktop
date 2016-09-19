# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import QListWidget
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
from datetime import datetime


class QMessageBoxWidget(QListWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setFont(QFont('Monospace', 12))
        # Запрещаем добавлять троеточие в месте обрезания строки
        self.setTextElideMode(Qt.ElideNone)
        # Нужно для переноса строк
        self.setWordWrap(True)

    def add_message(self, message):
        dt = datetime.fromtimestamp(int(message['time']) / 1000)
        self.addItem('[%s] %s: %s' % (
            dt.strftime('%H:%M:%S'),
            message['username'],
            message['msg'])
        )
