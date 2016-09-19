# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import QListWidget
from PyQt5.QtGui import QIcon
#from PyQt5.QtCore import *


class QUserListWidget(QListWidget):
    def __init__(self, *args, **kwargs):
        # Возможно sorted_users тут не так уж и нужно,
        # но пока пусть остается для удобства
        super().__init__(*args, **kwargs)
        self.afk_icon = QIcon('icons/afk.png')
        self.empty_icon = QIcon()
        self.users = {}
        self.sorted_users = []

    def __get_user_index(self, user_name):
        for index, user in enumerate(self.sorted_users):
            if user['name'] != user_name:
                continue
            return index

    def __sort_users(self):
        # сортировка по рангу/имени
        self.sorted_users = sorted(
            self.sorted_users,
            key=lambda u: (-u['rank'], u['name'].lower())
        )

    @property
    def styles(self):
        return '''
            QUserListWidget {
                background-color: black;
            }
    
            QUserListWidget::Item {
                color: white;
                background-color: black;
                selection-color: yellow;
            }
        '''

    def init_users(self, users):
        self.sorted_users = users
        self.__sort_users()
        for user in users:
            self.users[user['name']] = {
                'rank': user.get('rank', -1),
                'profile': user.get('profile', {}),
                'meta': user.get('meta', {})
            }
        
        for user in self.sorted_users:
            self.addItem(user['name'])
            if user.get('meta', {}).get('afk', False):
                self.item(self.count() - 1).setIcon(self.afk_icon)

    def delete_user(self, user):
        del self.users[user['name']]
        user_index = self.__get_user_index(user['name'])
        del self.sorted_users[user_index]
        self.removeItemWidget(self.takeItem(user_index))

    def add_user(self, user):
        self.users[user['name']] = {
            'rank': user.get('rank', -1),
            'profile': user.get('profile', {}),
            'meta': user.get('meta', {})
        }
        self.sorted_users.append(user)
        self.__sort_users()
        user_index = self.__get_user_index(user['name'])
        self.insertItem(user_index, user['name'])
        if user.get('meta', {}).get('afk', False):
            self.item(user_index).setIcon(self.afk_icon)

    def set_afk(self, user):
        user_index = self.__get_user_index(user['name'])
        if user.get('afk', False):
            self.item(user_index).setIcon(self.afk_icon)
        else:
            self.item(user_index).setIcon(self.empty_icon)

