
from .constants import K_T_ENGLISH as K_T
from .constants import K_F_ENGLISH as K_F
from .constants import K_S_ENGLISH as K_S
from .constants import K_O
from .constants import K_W_GRATE_ENGLISH as K_W_GRATE
from .constants import K_W_CURB_ENGLISH as K_W_CURB
from .constants import G_ENGLISH as G


class Node(object):

    def __init__(self, gutter):
        self.gutter = gutter

    def efficiency(self):
        return 0

    def intercepted(self, flow):
        eff = self.efficiency(flow)
        return eff*flow

    def bypass(self, flow):
        inter = self.intercepted(flow)
        return flow - inter


class Inlet(Node):

    def __init__(self, gutter, width):
        super().__init__(gutter)
        self.width = width

    def frontal_ratio(self, flow):
        spread = self.gutter.spread(flow)
        e_0 = self.gutter.flow_ratio(spread, self.width)
        if self.width < self.gutter.width:
            a_i = self.gutter.area_from_spread(self.width)
            a_g = self.gutter.area_from_spread(self.gutter.width)
            e_0 = e_0 * a_i / a_g
        return e_0

    def efficiency(self, flow):
        return 0.0

    def capacity(self, flow):
        return flow * self.efficiency(flow)


class CurbInlet(Inlet):

    def __init__(self, gutter, width, depth=0.0, length=0.0):
        super().__init__(gutter, width)
        self.depth = depth
        self.length = length

    def camber_eq(self, flow):
        e_0 = self.frontal_ratio(flow)
        return self.gutter.camber + self.depth/self.width * e_0

    def length_intercept(self, flow):
        s_e = self.camber_eq(flow)
        n = self.gutter.n
        return K_T * flow**0.42 * self.gutter.slope**0.3 * (1/(n * s_e))**0.6

    def efficiency(self, flow):
        l_t = self.length_intercept(flow)
        return min(1 - (1 - self.length/l_t)**1.8, 1)

    def head_normal(self, flow):
        gutter_head = self.gutter.head(flow)
        return gutter_head + self.gutter.depth

    def head_full(self, flow):
        return self.head_normal(flow) - self.depth

    def sag_capacity_weir(self, flow):
        h = self.head_normal(flow)
        p = self.length + 1.8*self.width
        return K_W_CURB * p * h**1.5

    def sag_capacity(self, flow):
        return self.sag_capacity_weir(flow)


class Grate(object):

    '''
    def __init__(self, a, b, c, d):
        self.a = a
        self.b = b
        self.c = c
        self.d = d

    def splash_velocity(self, length):
        return self.a + self.b*length - self.c*length**2 + self.d*length**3
    '''

    def __init__(self, coefficients=[]):
        self.coefficients = coefficients

    def splash_velocity(self, length):
        v_0 = 0.0
        for i, c in enumerate(self.coefficients):
            v_0 += c * length**i
        return v_0


class GrateInlet(Inlet):

    def __init__(self, gutter, width, length, grate=None):
        super().__init__(gutter, width)
        self.length = length
        self.grate = grate

    @property
    def grate_drop(self):
        if self.width > self.gutter.width:
            return self.width*self.gutter.camber + self.depth
        return self.width * self.gutter.depression_camber

    def frontal_flow_efficiency(self, flow):
        velocity = self.gutter.velocity(flow)
        v_0 = velocity
        if self.grate:
            v_0 = self.grate.splash_velocity(self.length)
        return min(1 - K_F * (velocity-v_0), 1.0)  # cannot exceed 1

    def side_flow_efficiency(self, flow):
        v = self.gutter.velocity(flow)
        camber = self.gutter.camber
        return 1 / (1 + (K_S * v**1.8) / (camber * self.length**2.3))

    def efficiency(self, flow):
        e_0 = self.frontal_ratio(flow)
        r_f = self.frontal_flow_efficiency(flow)
        r_s = self.side_flow_efficiency(flow)
        return min(r_f*e_0 + r_s * (1-e_0), 1.0)

    def sag_capacity_weir(self, flow):
        h = self.head(flow)
        p = 2*self.width + self.length
        return K_W_GRATE * p * h**1.5

    def sag_capacity_orifice(self, flow):
        h1 = self.head(flow)
        h = h1 + self.grate_drop/2
        return K_O * 1.0 * (2*G*h)**0.5

    def sag_capacity(self, flow):
        s_w = self.sag_capacity_weir(flow)
        s_o = self.sag_capacity_orifice(flow)
        return min(s_w, s_o)
