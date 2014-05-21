#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
pkgsetcomp module

"""

def __read_version_txt():
    import os.path
    SETUPPY_PATH = os.path.abspath(
        os.path.join(os.path.basename(__file__), '..'))
    with open(os.path.join(SETUPPY_PATH, 'VERSION.txt')) as f:
        version = f.read().strip()
    return version


global __version__
global version
version = __version__ = __read_version_txt()

#__ALL__ = ['pkgsetcomp', 'version', '__version__']
