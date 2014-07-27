from datetime import timedelta

class Period(object):
    @staticmethod
    def generate(code):
        return globals()[code]()

    def toTimeDelta(self):
        raise NotImplementedError("Should have implemented this")

    def __str__(self):
        return self.code

    # -------------------------------- properties -------------------

    @property
    def code(self):
        return self._code

class S5(Period):
    def __init__(self):
        self._code = 'S5'

    def toTimeDelta(self):
        return timedelta(0, 5)

class S10(Period):
    def __init__(self):
        self._code = 'S10'

    def toTimeDelta(self):
        return timedelta(0, 10)

class M1(Period):
    def __init__(self):
        self._code = 'M1'

    def toTimeDelta(self):
        return timedelta(0, 60)

class M30(Period):
    def __init__(self):
        self._code = 'M30'

    def toTimeDelta(self):
        return timedelta(0, 30 * 60)

class H1(Period):
    def __init__(self):
        self._code = 'H1'

    def toTimeDelta(self):
        return timedelta(0, 60 * 60)

class H2(Period):
    def __init__(self):
        self._code = 'H2'

    def toTimeDelta(self):
        return timedelta(0, 120 * 60)

class H4(Period):
    def __init__(self):
        self._code = 'H4'

    def toTimeDelta(self):
        return timedelta(0, 240 * 60)

class H8(Period):
    def __init__(self):
        self._code = 'H8'

    def toTimeDelta(self):
        return timedelta(0, 480 * 60)

class H12(Period):
    def __init__(self):
        self._code = 'H12'

    def toTimeDelta(self):
        return timedelta(0, 960 * 60)

class D(Period):
    def __init__(self):
        self._code = 'D'

    def toTimeDelta(self):
        return timedelta(1, 0)