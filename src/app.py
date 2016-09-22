# -*- coding: utf-8 -*-
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QHBoxLayout, QVBoxLayout, \
    QPushButton, QFrame
from PyQt5.QtCore import QObject, QThread, pyqtSignal, pyqtSlot
from src.widgets.QUserListWidget import QUserListWidget
from src.widgets.QMessageBoxWidget import QMessageBoxWidget
from src.widgets.QEditBoxWidget import QEditBoxWidget
from src.adapter.socket_io_bridge import socket_io_connection


class Worker(QObject):
    finished = pyqtSignal()
    chat_msg = pyqtSignal('PyQt_PyObject')
    add_user = pyqtSignal('PyQt_PyObject')
    user_leave = pyqtSignal('PyQt_PyObject')
    user_list = pyqtSignal('PyQt_PyObject')
    user_afk = pyqtSignal('PyQt_PyObject')
    init_smiles = pyqtSignal('PyQt_PyObject')
 
    @pyqtSlot()
    def process(self):
        socket_io_connection.connect(self)
        self.finished.emit()

    @pyqtSlot(object)
    def send_message(self, message):
        socket_io_connection.send_message(message)


class Application(QObject):
    #send_message_signal = pyqtSignal(object)

    def __init__(self):
        super().__init__()
        self.app = QApplication(sys.argv)
        self.window = QWidget()
        self.window.resize(854, 480)
        self.window.setWindowTitle("Animach")

        self.main_layout = QVBoxLayout(self.window)

        self.top_layout = QHBoxLayout()
        self.userlist = QUserListWidget(self.window)
        self.message_box = QMessageBoxWidget(self.window)

        self.userlist.itemClicked.connect(self.__select_user)

        self.top_layout.addWidget(self.userlist)
        self.top_layout.addWidget(self.message_box)

        self.bottom_layout = QHBoxLayout()
        self.edit_box = QEditBoxWidget(self, self.window)
        self.vertical_line = QFrame(self.window)
        self.vertical_line.setFixedWidth(10)
        self.send_btn = QPushButton(self.window)
        self.send_btn.setText('Send')

        self.send_btn.clicked.connect(self.send_message)

        self.send_btn.setFixedWidth(60)
        self.send_btn.setFixedHeight(60)

        self.bottom_layout.addWidget(self.edit_box)
        self.bottom_layout.addWidget(self.vertical_line)
        self.bottom_layout.addWidget(self.send_btn)

        self.main_layout.addItem(self.top_layout)
        self.main_layout.addItem(self.bottom_layout)

        self.window.setLayout(self.main_layout)
        self.__set_styles()

    def send_message(self):
        text = self.edit_box.toPlainText()
        if text:
            self.edit_box.clear()
            # FIXME: по уму это должно работать через сигналы,
            # но почему-то не взлетело
            #self.send_message_signal.emit(text)
            socket_io_connection.send_message(text)

    def __select_user(self, user_item):
        text = self.edit_box.toPlainText()
        user_name = user_item.text()
        if user_name not in text:
            self.edit_box.setText('%s: %s' % (user_name, text))

    def __set_styles(self):
        self.app.setStyleSheet('''
            QTextEdit {
                background-color: #010A01;
                color: white;
            }

            QListWidget {
                background-color: #010A01;
            }
    
            QListWidget::Item {
                background-color: #010A01;
                selection-color: yellow;
            }
            
            QMessageBoxWidget {
                color: white;
            }
            
            QUserListWidget {
                font: bold 16px "Monospace";
            }
        ''')


    # ==========================================================================
    # == Manage user methods ===================================================
    # ==========================================================================
    def init_users(self, users):
        self.userlist.init_users(users)

    def delete_user(self, user):
        self.userlist.delete_user(user)

    def add_user(self, user):
        self.userlist.add_user(user)

    def set_afk(self, user):
        self.userlist.set_afk(user)
    # ==========================================================================
    # ==========================================================================    

    def add_message(self, message):
        self.message_box.add_message(message)

    def init_smiles(self, smiles):
        self.message_box.init_smiles(smiles)

    def run(self):
        self.worker = Worker()
        self.thread = QThread(self.window)

        self.worker.moveToThread(self.thread)
        self.thread.started.connect(self.worker.process)
        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)

        self.worker.user_list.connect(self.init_users)
        self.worker.add_user.connect(self.add_user)
        self.worker.chat_msg.connect(self.add_message)
        self.worker.user_leave.connect(self.delete_user)
        self.worker.user_afk.connect(self.set_afk)
        self.worker.init_smiles.connect(self.init_smiles)

        self.thread.start()

        self.window.show()
        sys.exit(self.app.exec_())


app = Application()

