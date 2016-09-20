# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import QListWidget
from PyQt5.QtGui import QFont, QImage
from PyQt5.QtCore import Qt
from datetime import datetime
import config
import os


class QMessageBoxWidget(QListWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setFont(QFont('Monospace', 12))
        # Запрещаем добавлять троеточие в месте обрезания строки
        self.setTextElideMode(Qt.ElideNone)
        # Нужно для переноса строк
        self.setWordWrap(True)
        self.smiles = {}

    def add_message(self, message):
        dt = datetime.fromtimestamp(int(message['time']) / 1000)
        self.addItem('[%s] %s: %s' % (
            dt.strftime('%H:%M:%S'),
            message['username'],
            message['msg'])
        )
    
    def init_smiles(self, smiles):
        for smile in smiles:
            file_name = os.path.basename(smile['image'])
            self.smiles[smile['name']] = QImage(os.path.join(
                config.SMILES_LOCAL_DIR,
                file_name
            ))


