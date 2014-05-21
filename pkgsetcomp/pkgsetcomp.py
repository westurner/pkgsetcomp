#!/usr/bin/env python
# encoding: utf-8
from __future__ import print_function
"""
given
 * a list of default packages
 * a list of installed packages
 * apt-cache dependency graph

find the minimal set of packages that would install everything installed

costs:
 * time to generate solution

benefits:
 * (un) mark manually installed packages that are already dependencies
 * cool application of graph algorithms

See Also:

 * apt-clone

References:

* http://unix.stackexchange.com/a/3624

"""

import collections
import subprocess
import os
import shutil

here = os.path.join(os.path.dirname(__file__))

# MANIFEST_URL = (
# "http://mirror.pnl.gov/releases/12.04/ubuntu-12.04.4-desktop-i386.manifest"
# )
MANIFEST_URL = os.path.join(here, '..', 'tests', "testdata",
                            "ubuntu-12.04.4-desktop-i386.manifest")


def ensure_file(command, filename, overwrite=False, shell=False):
    """
    Run a command if a file doesn't exist

    Args:
        command (str): shell command to subprocess.call
        filename (str): path to os.path.exists
        overwrite (bool): if true, overwrite existing file
        shell (bool): subprocess command parsing
    Returns:
        None

    """
    print(command)
    if overwrite or not os.path.exists(filename):
        ret = subprocess.call(command, shell=shell)
        if ret:
            raise Exception(ret)
        return ret


def read_lines(filename):
    """
    Read and format lines of a file

    Args:
        filename (str): path to file to open as read-only
    Returns:
        generator of lines

    .. note:: this method is not unicode compatible
    """
    with file(filename) as f:
        for line in f:
            _line = line.strip()
            if _line:
                yield _line


def get_package_lists(manifest_url=MANIFEST_URL, cache=False, output_dir=None):
    """
    Get list of installed packages and manifest packages

    Generate:
        installed.pkgs.txt
        manifest.pkgs.txt

    Args:
        cache (bool): whether to cache
    Returns:
        tuple of lists: (installed, manifest)


    .. note:: adapted from: http://unix.stackexchange.com/a/3624
    """

    installed = get_installed_packages(cache=cache,
                                       output_dir=output_dir)
    manifest = get_manifest_packages(manifest_url=manifest_url,
                                     cache=cache,
                                     output_dir=output_dir)

    return installed, manifest


def get_installed_packages(cache=False,
                           output_dir='.',
                           output_filename='installed.pkgs.txt'):
    """
    Get a list of the packages in a manifest

    Args:
        manifest_url (str): path or URL of a debian/ubuntu .manifest file

    Returns:


    """
    output = os.path.join(output_dir, output_filename)
    cmd = '''aptitude search '~i !~M' -F '%%p' | sort -u > %r''' % (
        output)
    ensure_file(cmd, output, shell=True, overwrite=not(cache))
    installed = list(read_lines(output))
    return installed


def get_manifest_packages(cache=False,
                          manifest_url=None,
                          output_dir='.',
                          output_filename='manifest.pkgs.txt'):
    """
    Get a list of the packages in a manifest

    Args:
        manifest_url (str): path or URL of a debian/ubuntu .manifest file

    Returns:

    """
    output = os.path.join(output_dir, output_filename)
    cmd = ('''(wget -qO - %r || cat %r)'''
           ''' | awk '{ print $1 }' '''
           ''' | sort -u > %r''' % (manifest_url, manifest_url, output))
    ensure_file(cmd, output, shell=True, overwrite=not(cache))
    manifest = list(read_lines(output))
    return manifest


def import_apt():
    """
    import apt

    Returns:
        module: apt module
    """
    # 'least technical debt' solution
    # import apt_pkg
    try:
        import apt
    except ImportError:
        dist_packages = '/usr/lib/python2.7/dist-packages/'
        import sys
        import os
        import tempfile
        tmp_dirname = tempfile.mkdtemp()

        for modname in ('apt', 'apt_pkg.so'):
            module = os.path.join(dist_packages, modname)
            tmpdir_module = os.path.join(tmp_dirname, modname)
            os.symlink(module, tmpdir_module)

        sys.path.insert(0, tmp_dirname)
        import apt
        apt._tmp_dirname = tmp_dirname
    return apt


class PkgComparison(collections.namedtuple('PkgComparison', (
        'minimal',
        'also_installed',
        'uninstalled',
        'manifest',
        'installed'))):

    """
    A package set comparison namedtuple with serializers
    """

    def print_string(self):
        """
        Print the minimal, also_installed, and uninstalled lists
        """
        for x in self.minimal:
            print("min: %s" % x)
        for x in self.also_installed:
            print("als: %s" % x)
        for x in self.uninstalled:
            print("uni: %s" % x)

    def write_package_scripts(self, output_dir):
        """
        Generate boilerplate apt-get command scripts
        for minimal, also_installed, and uninstalled

        Args:
            output_dir (str): directory in which to write scripts
        """
        manifest_sh = os.path.join(output_dir, 'manifest.pkgs.sh')
        installed_sh = os.path.join(output_dir, 'installed.pkgs.sh')

        minimal_sh = os.path.join(output_dir, 'minimal.pkgs.sh')
        also_installed_sh = os.path.join(output_dir, 'also_installed.pkgs.sh')
        uninstalled_sh = os.path.join(output_dir, 'uninstalled.pkgs.sh')

        with open(manifest_sh, 'w') as f:
            for pkgname in self.manifest:
                print("manifest: %s" % pkgname)
                f.write("apt-get install %s" % pkgname)
                f.write("\n")
        with open(installed_sh, 'w') as f:
            for pkgname in self.manifest:
                print("installed: %s" % pkgname)
                f.write("apt-get install %s" % pkgname)
                f.write("\n")

        with open(minimal_sh, 'w') as f:
            for pkgname in self.minimal:
                print("min: %s" % pkgname)
                f.write("apt-get install %s" % pkgname)
                f.write("\n")
        with open(also_installed_sh, 'w') as f:
            for pkgname in self.also_installed:
                print("als: %s" % pkgname)
                f.write("apt-get install %s" % pkgname)
                f.write("\n")
        with open(uninstalled_sh, 'w') as f:
            for pkgname in self.uninstalled:
                print("uni: %s" % pkgname)
                f.write("apt-get remove %s" % pkgname)
                f.write("\n")


def compare_package_lists(manifest, installed):
    """
    Compare two sets (manifest, installed) of package names.

    Args:
        default (iterable): names of packages listed in a given MANIFEST
        installed (iterable): names of packages installed locally

    Returns:
        PkgComparison: set comparison outputs
    """

    uninstalled = [x for x in manifest if x not in installed]

    # == comm -23
    also_installed = [x for x in installed if x not in manifest]

    # 'easiest' solution
    # print "apt-get remove -y %s" % (' '.join(uninstalled))
    # print "apt-get install -y %s" % (' '.join(also_installed))

    # >>> why isn't this good enough?
    # <<< why manually install dependencies that may change?
    # <<< better to select the minimal graph/set/covering
    # <<< though apt-get will just re-compute these dependencies again
    # <<< "i swear i didn't manually install [...]"

    # stack = collections.dequeue()
    def visit_graph(apt_cache, pkgname, depends, visited):
        try:
            pkg = apt_cache[pkgname]
        except KeyError as e:
            print(e)  # TODO
            return

        for pkgset in pkg.installedDependencies:
            for pkg in pkgset:
                depends[pkg.name].append(pkgname)
                if pkgname not in visited:
                    visited[pkgname] = True
                    visit_graph(apt_cache, pkg.name, depends, visited)
                # stack.push( pkg['name'] )

    try:
        apt = import_apt()
        apt_cache = apt.Cache()

        depends = collections.defaultdict(list)
        visited = {}
        for pkgname in also_installed:
            visit_graph(apt_cache, pkgname, depends, visited)

        # TODO: more optimal covering
        minimal = [x for x in also_installed if x not in depends]
    finally:
        tmp_dir = getattr(apt, '_tmp_dirname')
        if tmp_dir and os.path.exists(tmp_dir):
            shutil.rmtree(apt._tmp_dirname)

    return PkgComparison(
        minimal,
        also_installed,
        uninstalled,
        manifest,
        installed)


def pkgsetcomp_packages_with_manifest(manifest_url, output_dir):
    """
    Compare installed packages with manifest packages

    Args:
        manifest_url (str): URL (or local path) to a debian/ubuntu .manifest
        output_dir (str): directory in which to write .pkg.sh and pkg.txt files

    Returns:
        PkgComparison: output of compare_package_lists
    """

    installed, default = get_package_lists(
        manifest_url=manifest_url,
        cache=True,
        output_dir=output_dir)

    comparison = compare_package_lists(default, installed)

    comparison.print_string()

    comparison.write_package_scripts(output_dir=output_dir)

    return comparison


def main():
    """
    pksetcomp main method (CLI)
    """
    import optparse
    import logging

    prs = optparse.OptionParser(usage="./%prog : [-o <path>] [-m <path/URL>]")

    prs.add_option('-m', '--manifest',
                   dest='manifest',
                   action='store',
                   help='PATH or URL to a debian/ubuntu .manifest',
                   default=MANIFEST_URL)

    prs.add_option('-o', '--output-dir',
                   dest='output_dir',
                   action='store',
                   help="Directory in which to store package lists",
                   default='.')

    prs.add_option('-v', '--verbose',
                   dest='verbose',
                   action='store_true',)
    prs.add_option('-q', '--quiet',
                   dest='quiet',
                   action='store_true',)

    (opts, args) = prs.parse_args()

    if not opts.quiet:
        logging.basicConfig()

        if opts.verbose:
            logging.getLogger().setLevel(logging.DEBUG)

    return pkgsetcomp_packages_with_manifest(opts.manifest, opts.output_dir)

if __name__ == "__main__":
    import sys
    sys.exit(main())
