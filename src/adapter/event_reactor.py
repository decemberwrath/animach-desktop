# -*- coding: utf-8 -*-
from socketIO_client import BaseNamespace
import time
import config


def filter_message(msg):
    return msg

def getEventReactor(app):
    class EventReactor(BaseNamespace):
        def __init__(self, io, path):
            super().__init__(io, path)
            self.starttime = int(time.time() * 1000)
            self.name = config.LOGIN
            self.mod = config.MODFLAIR
            self.app = app

        def on_chatMsg(self, data):
            username = data['username']
            msg = data['msg']
            ts = data['time']
            meta = data['meta']

            msg = filter_message(msg)
            if msg is None:
                return

            if ts < self.starttime:
                return

            self.app.add_message(data)
            print('[%s] %s: %s' % (ts, username, msg))

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

        def sendmsg(self, message):
            msg = { 'msg': message, 'meta': {} }
            #if self.mod:
            #   msg['meta']['modflair'] = rank
            self.emit('chatMsg', msg)

    return EventReactor


