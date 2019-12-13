
class Range:
    def __init__(self, start, finish):
        self.start = start
        self.finish = finish
    def get_range(self):
        return self.start, self.finish
    def __str__(self):
        return str((self.start, self.finish))