class RA:
    def __init__(self, window):
        self.nv = 0
        self.l = [0]*window
        self.i = 0

    def add(self, other):
        self.nv += other - self.l[self.i%len(self.l)]
        self.l[self.i%len(self.l)] = other
        self.i += 1

    def __float__(self):
        return self.nv/len(self.l)

    def is_ready(self):
        return self.i >= len(self.l)