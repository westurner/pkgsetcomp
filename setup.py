#!/usr/bin/env python
# -*- coding: utf-8 -*-

import glob
import logging
import os
import subprocess
import sys


try:
    from setuptools import setup, Command
except ImportError:
    from distutils.core import setup, Command

CONFIG = {
    'debug': True,
    'logname': None,
    'logformat': '%(asctime)s %(name)s %(levelname)-5s %(message)s',
    'loglevel': logging.DEBUG,  # logging.INFO
}

logging.basicConfig(format=CONFIG['logformat'])
log = logging.getLogger(CONFIG['logname'])
log.setLevel(CONFIG['loglevel'])

SETUPPY_PATH = os.path.dirname(os.path.abspath(__file__)) or '.'
log.debug('SETUPPY_PATH: %s' % SETUPPY_PATH)


if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    sys.exit()


class PyTestCommand(Command):
    user_options = []
    description = "<TODO>"

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        cmd = [sys.executable,
               os.path.join(SETUPPY_PATH, 'runtests.py'),
               '-v']

        globstr = os.path.join(SETUPPY_PATH, 'tests/test_*.py')
        cmd.extend(glob.glob(globstr))

        cmdstr = ' '.join(cmd)
        print(cmdstr)
        log.info(cmdstr)

        errno = subprocess.call(cmd)
        raise SystemExit(errno)


def build_long_description():
    with open('README.rst') as f:
        readme = f.read()
    with open('HISTORY.rst') as f:
        history = f.read().replace('. :changelog:', '')
    with open('AUTHORS.rst') as f:
        authors = f.read()
    return readme + '\n\n' + history + '\n\n' + authors


install_requires = [
]

setup(
    name='pkgsetcomp',
    version='0.1.0',
    description=(
        'Compare packages listed in a debian/ubuntu APT '
        '.manifest with installed packages'),
    long_description=build_long_description(),
    author='Wes Turner',
    author_email='wes@wrd.nu',
    url='https://github.com/westurner/pkgsetcomp',
    download_url='https://github.com/westurner/pkgsetcomp/releases',
    packages=[
        'pkgsetcomp',
    ],
    package_dir={'pkgsetcomp':
                 'pkgsetcomp'},
    include_package_data=True,
    install_requires=install_requires,
    license="BSD",
    zip_safe=False,
    keywords='pkgsetcomp apt deb debian ubuntu',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.7',
    ],
    entry_points={
        'console_scripts': [
            'pkgsetcomp=pkgsetcomp.pkgsetcomp:main'
        ]
    },
    test_suite='tests',
    cmdclass={
        'test': PyTestCommand,
    }
)
