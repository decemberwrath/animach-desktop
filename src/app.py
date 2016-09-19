# -*- coding: utf-8 -*-
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QListWidget, QHBoxLayout
from PyQt5.QtCore import QObject, QThread, pyqtSignal, pyqtSlot
from src.widgets.QUserListWidget import QUserListWidget
from src.adapter.socket_io_bridge import SocketIOConnection


class Worker(QObject):
    finished = pyqtSignal()
    message = pyqtSignal(int)
 
    @pyqtSlot()
    def process(self):
        socket_io_conn = SocketIOConnection()
        socket_io_conn.connect(app)
        self.finished.emit()


class Application:
    def __init__(self):
        self.app = QApplication(sys.argv)

        self.window = QWidget()
        self.window.resize(640, 480)
        self.window.setWindowTitle("Animach")

        self.layout = QHBoxLayout(self.window)

        self.userlist = QUserListWidget(self.window)
        self.userlist.setMaximumWidth(200)
        self.message_box = QListWidget(self.window)

        self.layout.addWidget(self.userlist)
        self.layout.addWidget(self.message_box)

        self.window.setLayout(self.layout)

        self.__set_styles()

    def __set_styles(self):
        self.app.setStyleSheet(self.userlist.styles)

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
        self.message_box.addItem('[%s] %s: %s' % (
            message['time'], message['username'], message['msg'])
        )

    def run(self):
        self.thread = QThread(self.window)
        self.worker = Worker()
        self.worker.moveToThread(self.thread)
 
        self.thread.started.connect(self.worker.process)
        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)
        self.thread.start()

        self.window.show()
        sys.exit(self.app.exec_())


app = Application()

