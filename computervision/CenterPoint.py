
class CenterPoint:

    def __init__(self, key, px, py, x, y, z):
        self.key = key
        self.px = px
        self.py = py
        self.x = x
        self.y = y
        self.z = z

        print(key, px, py, x, y, z)

    def __str__(self):
        return self.key #+ ' ' + str(self.delay)