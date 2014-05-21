===============================
pkgsetcomp
===============================


`GitHub`_ |
`PyPi`_ |
`Warehouse`_ |
`ReadTheDocs`_ |
`Travis-CI`_


.. image:: https://badge.fury.io/py/pkgsetcomp.png
   :target: http://badge.fury.io/py/pkgsetcomp
    
.. image:: https://travis-ci.org/westurner/pkgsetcomp.png?branch=master
        :target: https://travis-ci.org/westurner/pkgsetcomp

.. image:: https://pypip.in/d/pkgsetcomp/badge.png
       :target: https://pypi.python.org/pypi/pkgsetcomp

.. _GitHub: https://github.com/westurner/pkgsetcomp
.. _PyPi: https://pypi.python.org/pypi/pkgsetcomp
.. _Warehouse: https://warehouse.python.org/project/pkgsetcomp
.. _ReadTheDocs:  https://pkgsetcomp.readthedocs.org/en/latest
.. _Travis-CI:  https://travis-ci.org/westurner/pkgsetcomp

pkgsetcomp: compare and generate manifest / installed package reports


Features
==========

* Compare packages listed in a debian/ubuntu APT `manifest file`_ with
  currently installed packages
* `optparse`_ argument parsing (``-h``, ``--help``)
* `cookiecutter-pypackage`_ project templating  


.. _manifest file: http://releases.ubuntu.com/14.04/ubuntu-14.04-desktop-i386.manifest
.. _optparse: https://docs.python.org/2/library/optparse.html 
.. _cookiecutter-pypackage: https://github.com/audreyr/cookiecutter-pypackage 



Installing
============
Install from `PyPi`_::

    pip install pkgsetcomp

Install from `GitHub`_ as editable (add a ``pkgsetcomp.pth`` in ``site-packages``)::

    pip install -e git+https://github.com/westurner/pkgsetcomp#egg=pkgsetcomp


Usage
=========

Print help::

    pkgsetcomp --help

Generate reports in the current directory::

    pkgsetcomp

Generate a report comparing against a specified manifest file:

    MANIFEST="http://releases.ubuntu.com/14.04/ubuntu-14.04-desktop-amd64.manifest"
    pkgsetcomp --manifest="$MANIFEST"

License
========
`BSD Software License
<https://github.com/westurner/pkgsetcomp/blob/master/LICENSE>`_
