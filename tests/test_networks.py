
import unittest

from pyhec22.networks import Network
from pyhec22.gutters import Gutter
from pyhec22.exceptions import NotConfluent


class NetworkTest(unittest.TestCase):

    def setUp(self):
        self.g1 = Gutter(camber=0.02, n=0.016, slope=0.01)
        self.g2 = Gutter(camber=0.02, n=0.016, slope=0.01)
        self.g3 = Gutter(camber=0.02, n=0.016, slope=0.01)
        self.g4 = Gutter(camber=0.02, n=0.016, slope=0.01)

    def test_circular_references(self):
        links = [
            (self.g1, self.g2),
            (self.g2, self.g3),
            (self.g3, self.g1),
        ]
        with self.assertRaises(NotConfluent):
            Network(links)

    def test_gutter_with_two_bypasses(self):
        links = [
            (self.g1, self.g2),
            (self.g2, self.g3),
            (self.g2, self.g4),
        ]
        with self.assertRaises(NotConfluent):
            Network(links)

    def test_gutter_with_converging_bypasses(self):
        links = [
            (self.g1, self.g3),
            (self.g2, self.g3),
            (self.g3, self.g4),
        ]
        try:
            Network(links)
        except NotConfluent:
            self.fail("aised NotConfluent unexpectedly!")

    def test_linear_network(self):
        links = [
            (self.g1, self.g2),
            (self.g2, self.g3),
            (self.g3, self.g4),
        ]
        try:
            Network(links)
        except NotConfluent:
            self.fail("aised NotConfluent unexpectedly!")
