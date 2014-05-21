

import shutil
import tempfile
import unittest

from pkgsetcomp import pkgsetcomp


class Test_pkgsetcomp(unittest.TestCase):

    def setUp(self):
        self.output_dir = tempfile.mkdtemp(prefix='compare_paths_')

    def tearDown(self):
        shutil.rmtree(self.output_dir)

    def test_00_pkgsetcomp(self):
        manifest = ['orange', 'carrot', 'corn']
        installed = ['apple', 'orange', 'peach']

        comparison = pkgsetcomp.compare_package_lists(manifest, installed)

        comparison.print_string()

        self.assertEqual(comparison.uninstalled, ['carrot', 'corn'])
        self.assertEqual(comparison.installed, installed)
        self.assertEqual(comparison.manifest, manifest)
        self.assertEqual(comparison.also_installed, ['apple', 'peach'])

        # self.assertEqual(comparison.minimal, ['...'])

        comparison.write_package_scripts(self.output_dir)

        # raise Exception()

    def test_10_get_package_lists(self):
        installed, manifest = pkgsetcomp.get_package_lists(
            output_dir=self.output_dir)
        assert isinstance(installed, list)
        assert isinstance(manifest, list)
        self.assertTrue(len(installed))
        self.assertTrue(len(manifest))

    def test_20_compare_live_system(self):
        comparison = pkgsetcomp.pkgsetcomp_packages_with_manifest(
            pkgsetcomp.MANIFEST_URL,
            self.output_dir)

        self.assertTrue(comparison.manifest)
        self.assertTrue(comparison.installed)
        self.assertTrue(len(comparison.manifest))
        self.assertTrue(len(comparison.installed))

        # self.assertTrue(len(comparison.also_installed))
        # self.assertTrue(len(comparison.minimal))
        # self.assertTrue(len(comparison.uninstalled))

if __name__ == "__main__":
    import sys
    sys.exit(unittest.main())
