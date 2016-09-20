# -*- coding: utf-8 -*-
import os


DOMAIN = 'test.com'

CHANNEL = 'main'

CHANNELPASS = None

LOGIN = 'test'

PASSWORD = 'testpasswd'

MODFLAIR = False

ICONS_LOCAL_DIR = 'icons'

SMILES_LOCAL_DIR = 'smiles'

SMILES_DIR = os.path.join(
    os.path.dirname(os.path.realpath(__file__)),
    SMILES_LOCAL_DIR
)


try:
    from config_local import *
except:
    pass
