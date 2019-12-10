class Position:
    def __init__(self, m0, m1, m2):
        self.m0 = m0
        self.m1 = m1
        self.m2 = m2

    def __str__(self):
        return str(self.m0) + ' ' + str(self.m1) + ' ' + str(self.m2)