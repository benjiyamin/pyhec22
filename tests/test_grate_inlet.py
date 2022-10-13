
import unittest

from pyhec22.gutters import Gutter
from pyhec22.inlets import GrateInlet


class GrateInletTest(unittest.TestCase):

    def setUp(self):
        self.composite_gutter = Gutter(
            camber=0.02, n=0.016, slope=0.01, width=2.0, depth=2/12)
        self.composite_gutter_grate_inlet = GrateInlet(
            self.composite_gutter, width=2.0, length=2.0)
        self.simple_gutter = Gutter(camber=0.025, n=0.016, slope=0.04)
        self.simple_gutter_grate_inlet = GrateInlet(
            self.simple_gutter, width=2.0, length=2.0)

    def test_composite_gutter_velocity(self):
        """Example 4-7 Step 1 (English Units)"""
        g = self.composite_gutter
        flow = 2.3  # cfs
        produced = g.velocity(flow)
        expected = 2.75
        self.assertAlmostEqual(produced, expected, 2)

    def test_grate_inlet_frontal_flow_efficiency(self):
        """Example 4-7 Step 2 (English Units)"""
        i = self.composite_gutter_grate_inlet
        flow = 2.3  # cfs
        produced = i.frontal_flow_efficiency(flow)
        expected = 1.0
        self.assertEqual(produced, expected)

    def test_grate_inlet_side_flow_efficiency(self):
        """Example 4-7 Step 3 (English Units)"""
        i = self.composite_gutter_grate_inlet
        flow = 2.3  # cfs
        produced = i.side_flow_efficiency(flow)
        expected = 0.1
        self.assertAlmostEqual(produced, expected, 1)

    def test_grate_inlet_intercepted(self):
        """Example 4-7 Step 4 (English Units)"""
        i = self.composite_gutter_grate_inlet
        flow = 2.3  # cfs
        produced = i.intercepted(flow)
        expected = 1.7
        self.assertAlmostEqual(produced, expected, 1)

    def test_simple_gutter_flow(self):
        """Example 4-8 Step 1 (English Units)"""
        g = self.simple_gutter
        spread = 9.84  # ft
        produced = g.flow(spread)
        expected = 6.65
        self.assertAlmostEqual(produced, expected, 2)

    def test_simple_gutter_grate_inlet_frontal_ratio(self):
        """Example 4-8 Step 2 (English Units)"""
        i = self.simple_gutter_grate_inlet
        spread = 9.84  # ft
        flow = i.gutter.flow(spread)
        produced = i.frontal_ratio(flow)
        expected = 0.45
        self.assertAlmostEqual(produced, expected, 2)

    def test_simple_gutter_grate_inlet_gutter_flow_velocity(self):
        """Example 4-8 Step 3 (English Units)"""
        i = self.simple_gutter_grate_inlet
        spread = 9.84  # ft
        flow = i.gutter.flow(spread)
        produced = i.gutter.velocity(flow)
        expected = 5.5  # fps
        self.assertAlmostEqual(produced, expected, 1)

    '''
    def test_simple_gutter_grate_inlet_capacity_1(self):
        """Example 4-8 Step 1 Row 1 (English Units)"""
        # reticuline = Grate(0.28, 2.28, 0.18, 0.01)
        reticuline = Grate([0.28, 2.28, -0.18, 0.01])
        i = GrateInlet(
            gutter=self.simple_gutter, width=2.0, length=2.0, grate=reticuline)
        spread = 9.84 # ft
        flow = i.gutter.flow(spread)
        produced = i.capacity(flow)
        expected = 3.21  # fps
        self.assertAlmostEqual(produced, expected, 2)
    '''
