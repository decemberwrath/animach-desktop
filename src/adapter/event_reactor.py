# -*- coding: utf-8 -*-
from socketIO_client import BaseNamespace


def filter_message(msg):
    return msg


def getEventReactor(app):
    class EventReactor(BaseNamespace):
        def __init__(self, io, path):
            super().__init__(io, path)
            self.app = app

        def on_chatMsg(self, message):
            msg = filter_message(message['msg'])
            self.app.add_message(message)

        def on_pm(self, data):
            ts = data['time']
            username = data['username']
            msg = data['msg']

            msg = filter_message(msg)
            if msg is None:
                return

            print('[%s] PRIVATE %s: %s' % (ts, username, msg))

        def on_addUser(self, new_user):
            app.add_user(new_user)

        def on_userLeave(self, user):
            app.delete_user(user)

        def on_userlist(self, users):
            app.init_users(users)

        def on_setAFK(self, user):
            if user and user.get('name', None):
                app.set_afk(user)

    return EventReactor


