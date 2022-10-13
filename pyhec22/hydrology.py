

class Basin(object):

    def __init__(self, area=0.0, c=0.0, **kwargs):
        self.area = area
        self.c = c
        shapes = kwargs.pop('shapes', [])
        if shapes:
            self.add_shapes(shapes)

    @property
    def runoff_area(self):
        return self.area * self.c

    def add_shapes(self, shapes):
        a_shp = sum(shp[0] for shp in shapes)
        c_shp = sum(shp[0] * shp[1] for shp in shapes) / a_shp
        a_tot = self.area + a_shp
        self.c = (self.area*self.c + a_shp*c_shp) / a_tot
        self.area = a_tot
