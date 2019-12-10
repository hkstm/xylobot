class Note:
    #   key = c6-c7
    #   delay in seconds
    def __init__(self, key, delay):
        self.key = key
        self.delay = delay

    def __str__(self):
        return self.key + ' ' + str(self.delay)