
class t_class:
    def __init__(self, x, y):
        self.x = x;  self.y = y
        #  Class is set up, and returned from here

    def __str__(self):
        print("from t_class: x %d, y %d" % (self.x,self.y))

    def xy(self, z):
        print("x %d, y %s, z %d" % (self.x, self.y, z))


tc = t_class(11, 22)

tc.xy(33)
