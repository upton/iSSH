#!/usr/bin/env python
# -*- coding: utf-8 -*-
from setuptools import setup

APP = ['iSSH.py']
DATA_FILES = ['hosts.txt',
              'auto_login.exp',
              'login.sh',
              'README.md',
              'LICENSE']
OPTIONS = {
    'argv_emulation': True,
    'plist': {
        'LSUIElement': True,
    },
    'packages': ['rumps'],
    'iconfile':'iSSH.icns'
}

setup(
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)
