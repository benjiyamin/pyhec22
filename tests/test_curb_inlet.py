
import unittest

from pyhec22.gutters import Gutter
from pyhec22.nodes import CurbInlet


class CurbInletTest(unittest.TestCase):

    def setUp(self):
        self.simple_gutter = Gutter(camber=0.02, n=0.016, slope=0.01)
        self.curb_inlet_no_depth = CurbInlet(
            gutter=self.simple_gutter, width=2.0, length=9.84)
        self.curb_inlet = CurbInlet(
            gutter=self.simple_gutter, width=2.0, length=9.84, depth=1/12)
        self.composite_gutter = Gutter(
            camber=0.02, n=0.016, slope=0.01, width=2.0, depth=2/12)
        self.composite_gutter_curb_inlet = CurbInlet(
            gutter=self.composite_gutter, width=2.0, length=9.84, depth=2/12)

    def test_curb_inlet_no_depth_length_intercept(self):
        """Example 4-9a (1) Step 1 (English Units)"""
        i = self.curb_inlet_no_depth
        flow = 1.77  # cfs
        produced = i.length_intercept(flow)
        expected = 23.94  # ft
        self.assertAlmostEqual(produced, expected, 2)

    def test_curb_inlet_no_depth_efficiency(self):
        """Example 4-9a (1) Step 2 (English Units)"""
        i = self.curb_inlet_no_depth
        flow = 1.77  # cfs
        produced = i.efficiency(flow)
        expected = 0.61
        self.assertAlmostEqual(produced, expected, 2)

    def test_curb_inlet_no_depth_capacity(self):
        """Example 4-9a (1) Step 3 (English Units)"""
        i = self.curb_inlet_no_depth
        flow = 1.77  # cfs
        produced = i.capacity(flow)
        expected = 1.09  # cfs
        self.assertAlmostEqual(produced, expected, 2)

    '''
    def test_gutter_upper_flow(self):
        """Example 4-9a (2) Step 1 (English Units)"""
        g = self.simple_gutter
        flow = 1.77 # cfs
        spread = g.spread(flow)
        produced = g.upper_flow(spread)
        expected = 0.69  # cfs
        self.assertAlmostEqual(produced, expected, 2)

    def test_curb_inlet_efficiency(self):
        """Example 4-9a (2) Step 2 (English Units)"""
        i = self.curb_inlet
        flow = 1.77 # cfs
        produced = i.efficiency(flow)
        expected = 0.88
        self.assertAlmostEqual(produced, expected, 2)
    '''

    def test_curb_inlet_eq_camber(self):
        """Example 4-9b Step 1 (English Units)"""
        i = self.composite_gutter_curb_inlet
        flow = 2.26  # cfs
        produced = i.camber_eq(flow)
        expected = 0.08
        self.assertAlmostEqual(produced, expected, 2)

    def test_curb_inlet_length_intercept(self):
        """Example 4-9b Step 2 (English Units)"""
        i = self.composite_gutter_curb_inlet
        flow = 2.26  # cfs
        produced = i.length_intercept(flow)
        expected = 11.6  # ft
        self.assertAlmostEqual(produced, expected, 1)
