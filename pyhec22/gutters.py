

from scipy import optimize

from .constants import K_U_ENGLISH as K_U


class Gutter(object):

    def __init__(self, camber, n, slope, depth=0.0, width=0.0):
        self.camber = camber
        self.n = n
        self.slope = slope
        self.depth = depth
        self.width = width

    @property
    def depression_camber(self):
        dc = self.camber
        if self.width > 0:
            dc += self.depth/self.width
        return dc

    @property
    def max_lower_flow(self):
        dc = self.depression_camber
        return K_U/self.n * dc**(5/3) * self.slope**0.5 * self.width**(8/3)

    def flow_ratio(self, spread, width=0.0):
        calc_width = self.width
        if width > 0.0:
            calc_width = width
        a = self.depression_camber / self.camber
        b = spread / calc_width
        c = (1 + (a / (b-1)))**(8/3)
        e_0 = 1 / (1 + a / (c-1))
        return e_0

    def upper_flow(self, spread):
        spread = spread - self.width
        c = self.camber
        return K_U/self.n * c**(5/3) * self.slope**0.5 * spread**(8/3)

    def lower_flow(self, spread):
        dc = self.depression_camber
        return K_U/self.n * dc**(5/3) * self.slope**0.5 * spread**(8/3)

    def flow(self, spread):
        if spread <= self.width:
            return self.lower_flow(spread)
        flow = self.upper_flow(spread)
        if self.width > 0:
            flow /= (1 - self.flow_ratio(spread))
        return flow

    def depression_flow(self, spread):
        return self.flow(spread) - self.upper_flow(spread)

    def spread_accuracy(self, spread, flow):
        return self.flow(spread) - flow

    def simple_spread(self, flow):
        c = self.camber
        return (flow*self.n/(K_U * c**(5/3) * self.slope**0.5))**(3/8)

    def lower_spread(self, flow):
        dc = self.depression_camber
        return (flow*self.n/(K_U * dc**(5/3) * self.slope**0.5))**(3/8)

    def spread(self, flow):
        if flow <= self.max_lower_flow:
            return self.lower_spread(flow)
        simple_spread = self.simple_spread(flow)
        if self.width == 0.0:
            return simple_spread
        return optimize.bisect(
            f=self.spread_accuracy,
            a=self.width + 1e-5,
            b=simple_spread,
            args=(flow,)
        )

    def head(self, flow):
        spread = self.spread(flow)
        if spread > self.width:
            return spread*self.camber + self.depth
        return spread * self.depression_camber

    def area_from_spread(self, spread):
        lower_area = self.depth * min(self.width, spread) / 2
        upper_area = self.camber * spread**2 / 2
        return lower_area + upper_area

    def area_from_flow(self, flow):
        spread = self.spread(flow)
        return self.area_from_spread(spread)

    def area(self, flow):
        return self.area_from_flow(flow)

    def velocity(self, flow):
        area = self.area_from_flow(flow)
        return flow / area
