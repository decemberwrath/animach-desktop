# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import QTextBrowser
from PyQt5.QtGui import QFont
from datetime import datetime
import config
import os
import re


def make_smile_text(smile):
    file_name = os.path.basename(smile['image'])
    smile_path = os.path.join(config.SMILES_LOCAL_DIR, file_name)
    # TODO: придумать что делать с анимацией
    # TODO: фиксировать максимальную высоту изображения (нет, max-height не работает)
    return '<img max-height=100 src="%s">' % smile_path


class QMessageBoxWidget(QTextBrowser):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setFont(QFont('Monospace', 12))
        self.smiles = {}
        self.smile_regex = re.compile(':(\w+):')

    def format_message(self, msg):
        # TODO: обработка спойлеров
        # TODO: обработка пользовательских изображений
        # обработка смайлов
        smiles_in_msg = self.smile_regex.findall(msg)
        smile_name = None
        for smile in smiles_in_msg:
            smile_name = ':%s:' % smile
            if not self.smiles.get(smile_name, None):
                continue
            msg = msg.replace(smile_name, self.smiles[smile_name])
        return msg

    def add_message(self, message):
        dt = datetime.fromtimestamp(int(message['time']) / 1000)
        self.append('[%s] <b>%s</b>: %s' % (
            dt.strftime('%H:%M:%S'),
            message['username'],
            self.format_message(message['msg']))
        )
    
    def init_smiles(self, smiles):
        for smile in smiles:
            self.smiles[smile['name']] = make_smile_text(smile)


