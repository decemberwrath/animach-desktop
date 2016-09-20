# -*- coding: utf-8 -*-
from socketIO_client import BaseNamespace
from src.adapter.utils import sync_smiles


def getEventReactor(bridge):
    class EventReactor(BaseNamespace):
        def __init__(self, io, path):
            super().__init__(io, path)
            self.bridge = bridge

        def on_chatMsg(self, message):
            self.bridge.chat_msg.emit(message)

        def on_pm(self, data):
            ts = data['time']
            username = data['username']
            msg = data['msg']
            if msg:
                print('[%s] PRIVATE %s: %s' % (ts, username, msg))

        def on_addUser(self, new_user):
            self.bridge.add_user.emit(new_user)

        def on_userLeave(self, user):
            self.bridge.user_leave.emit(user)

        def on_userlist(self, users):
            self.bridge.user_list.emit(users)

        def on_setAFK(self, user):
            self.bridge.user_afk.emit(user)
        
        def on_emoteList(self, smiles):
            sync_smiles(smiles)
            self.bridge.init_smiles.emit(smiles)

    return EventReactor


