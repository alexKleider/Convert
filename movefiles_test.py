#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# vim: set file encoding=utf-8 :
# Copyright 2014 Alex Kleider; All Rights Reserved.

# file: 'movefiles_test.py'
"""
Test mod_copy.move_files(old_dir, new_dir).
"""

import os
import sys
import shutil
import unittest
import mod_copy

class test_filemoving(unittest.TestCase):
    """Test mod_copy.move_files."""

    def setup(self):
        pass

    def test_virgin_system(self):
        self.assertTrue(os.path.isdir(mod_copy.ROOT_DIR))
        mod_copy.setup_directories(mod_copy.ROOT_DIR,
                                    mod_copy.NEW_ROOT_DIR)
        self.assertTrue(os.path.isdir(mod_copy.NEW_ROOT_DIR))
        os.rmdir(mod_copy.NEW_ROOT_DIR)
        self.assertFalse(os.path.isdir(mod_copy.NEW_ROOT_DIR))

    def test_traversal(self):
        mod_copy.setup_directories(mod_copy.ROOT_DIR,
                                    'Tree0')
        self.assertTrue(os.path.isdir('Tree0'))
        mod_copy.move_files('DirTree', 'Tree0')
#       shutil.rmtree('Tree0')

    def teardown():
        pass

if __name__ == "__main__":
    print("Running Python3 script: 'movefiles_test.py'.......")
    print('"""', end='')
    print(__doc__, end='')
    print('"""')
    unittest.main()


