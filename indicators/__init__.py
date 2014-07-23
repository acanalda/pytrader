class Indicator(object):
    def __init__(self):
        self._values = []

    @property
    def values(self):
        return self._values

    def update(self, instrument, cur_index):
        raise NotImplementedError("Should have implemented this")

    def getLast(self, n = 1):
        if n > 1:
            return self.values[-n:-(n-1)]
        else:
            return self.values[-1]

    def crossUp(self, indicator):
        return self.getLast(2) < indicator.getLast(2) and \
            self.getLast(1) > indicator.getLast(1)

    def crossDown(self, indicator):
        return self.getLast(2) > indicator.getLast(2) and \
            self.getLast(1) < indicator.getLast(1)