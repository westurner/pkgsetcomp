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
    user_options = [
        ("pdb", "p", "run with --pdb"),
        ("ipdb", "i", "run with --ipdb"),
        ("collect-only", "C", "collect but do not run the tests"),
        ("test-expr=", "k", "only run tests matching the expression"),
        ("report=", "r", "show extra test summary as specified by chars: "
         "(f)ailed, (E)rror, (s)kipped, (x)failed, (X)passed"),
        ("showlocals", "l", "show locals in tracebacks"),
        ("tb=", "t", "traceback print mode (long/short/line/native/no)"),
        ("full-trace", "T", "don't cut any tracebacks (default is to cut)"),
        ("color=", "c", "color terminal (yes/no/auto)"),
    ]
    description = "run: runtests.py -v <test_files>"

    def initialize_options(self):
        self.pdb = None
        self.ipdb = None
        self.collect_only = None
        self.test_expr = None
        self.report = None
        self.showlocals = None
        self.tb = None
        self.full_trace = None
        self.color = None
        self.pytest_args = []

    def finalize_options(self):
        if self.pdb:
            self.pytest_args.insert(0, '--pdb')
        if self.ipdb:
            self.pytest_args.insert(0, '--ipdb')
        if self.collect_only:
            self.pytest_args.insert(0, '--collect-only')
        if self.test_expr:
            self.pytest_args.insert(0, '-k %s' % self.test_expr)
        if self.report:
            self.pytest_args.insert(0, '--report=%s' % self.report)
        if self.showlocals:
            self.pytest_args.insert(0, '--showlocals')
        if self.tb:
            self.pytest_args.insert(0, '--tb=%s' % self.tb)
        if self.full_trace:
            self.pytest_args.insert(0, "--full-trace")
        if self.color:
            self.pytest_args.insert(0, "--color=%s" % self.color)

    def run(self):
        cmd = [sys.executable,
               os.path.join(SETUPPY_PATH, 'runtests.py'),
               '-v']

        cmd.extend(self.pytest_args)

        globstr = os.path.join(SETUPPY_PATH, 'tests/test_*.py')
        cmd.extend(glob.glob(globstr))

        cmdstr = ' '.join(cmd)
        print(cmdstr)
        log.info(cmdstr)

        errno = subprocess.call(cmd)
        raise SystemExit(errno)


def build_long_description():
    with open(os.path.join(SETUPPY_PATH, 'README.rst')) as f:
        readme = f.read()
    with open(os.path.join(SETUPPY_PATH, 'HISTORY.rst')) as f:
        history = f.read().replace('. :changelog:', '')
    with open(os.path.join(SETUPPY_PATH, 'AUTHORS.rst')) as f:
        authors = f.read()
    return readme + '\n\n' + history + '\n\n' + authors


def read_version_txt():
    with open(os.path.join(SETUPPY_PATH, 'VERSION.txt')) as f:
        version = f.read().strip()
    return version


install_requires = [
]

setup(
    name='pkgsetcomp',
    version=read_version_txt(),
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
