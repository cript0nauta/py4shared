#!/usr/bin/env python
#-*- coding: utf-8 -*-

from setuptools import setup #, find_packages

setup(name='py4shared',
        version = '1.0',
        description = '4shared download manager',
        author = 'Matías Lang',
        author_email = 'shareman1204@gmail.com',
        url = 'https://github.com/sh4r3m4n/py4shared',
        license = 'GPL3',
        scripts = ['py4shared.py'],
        py_modules = ['py4shared'],
        install_requires = ['requests', 'pyquery']
    )
