import sys
import unittest

import numpy as np

import daz


class TestDaz(unittest.TestCase):

    def setUp(self):
        self.scale = 128
        self.normal = sys.float_info.min
        self.denormal = sys.float_info.min / self.scale

    def check_normal(self):
        assert self.normal == self.denormal * self.scale
        assert self.normal / self.scale == self.denormal
        assert not daz.get_daz()
        assert not daz.get_ftz()

    def test_normal(self):
        self.check_normal()

    def test_daz(self):
        daz.set_daz()
        assert daz.get_daz()
        assert not daz.get_ftz()
        assert self.normal / self.scale == 0
        assert self.denormal * self.scale == 0
        assert self.denormal == 0
        daz.unset_daz()
        self.check_normal()

    def test_ftz(self):
        daz.set_ftz()
        assert daz.get_ftz()
        assert not daz.get_daz()
        assert self.normal / self.scale == 0
        assert self.denormal * self.scale == self.normal
        assert self.denormal != 0
        daz.unset_ftz()
        self.check_normal()


class TestDazWithNumPy(unittest.TestCase):

    def setUp(self):
        self.scale = 2
        self.normal = np.full((3,), sys.float_info.min)
        self.denormal = np.full((3,), sys.float_info.min) / self.scale

    def check_normal(self):
        np.testing.assert_equal(self.normal, self.denormal * self.scale)
        np.testing.assert_equal(self.normal / self.scale, self.denormal)

    def test_normal(self):
        self.check_normal()

    def test_daz(self):
        daz.set_daz()
        np.testing.assert_equal(self.normal / self.scale, 0)
        np.testing.assert_equal(self.denormal * self.scale, 0)
        np.testing.assert_equal(self.denormal, 0)
        daz.unset_daz()
        self.check_normal()

    def test_ftz(self):
        daz.set_ftz()
        np.testing.assert_equal(self.normal / self.scale, 0)
        np.testing.assert_equal(self.denormal * self.scale, self.normal)
        assert np.all(self.denormal != 0)
        daz.unset_ftz()
        self.check_normal()
