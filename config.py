# -*- coding: utf-8 -*-

DOMAIN = 'test.com'

CHANNEL = 'main'

CHANNELPASS = None

LOGIN = 'test'

PASSWORD = 'testpasswd'

MODFLAIR = False

try:
    from config_local import *
except:
    pass
