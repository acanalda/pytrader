from datetime import timedelta

class Currency(object):
    @property
    def code(self):
        return self._code

class EUR(Currency):
    def __init__(self):
        self._code = 'EUR'

class USD(Currency):
    def __init__(self):
        self._code = 'USD'

class JPY(Currency):
    def __init__(self):
        self._code = 'JPY'

class AUD(Currency):
    def __init__(self):
        self._code = 'AUD'

class CAD(Currency):
    def __init__(self):
        self._code = 'CAD'

class CHF(Currency):
    def __init__(self):
        self._code = 'CHF'

class GBP(Currency):
    def __init__(self):
        self._code = 'GBP'

""" ------------------- BAR ------------------- """
class Bar(object):
    CLOSE = 'close'
    OPEN = 'open'

    def __init__(self, obj):
        self._original = obj
        self._time = obj['time']
        self._open = (self.open_bid + self.open_ask) / 2
        self._close = (self.close_bid + self.close_ask) / 2
        self._high = (self.high_bid + self.high_ask) / 2
        self._low = (self.low_bid + self.low_ask) / 2

    # -------------------------------- properties -------------------

    @property
    def original(self):
        return self._original

    @property
    def time(self):
        return self._time

    @property
    def time_str(self):
        return self.original['time']

    @property
    def open(self):
        return self._open

    @property
    def open_bid(self):
        return self.original['openBid']

    @property
    def open_ask(self):
        return self.original['openAsk']

    @property
    def close(self):
        return self._close

    @property
    def close_bid(self):
        return self.original['closeBid']

    @property
    def close_ask(self):
        return self.original['closeAsk']

    @property
    def high(self):
        return self._high

    @property
    def high_bid(self):
        return self.original['highBid']

    @property
    def high_ask(self):
        return self.original['highAsk']

    @property
    def low(self):
        return self._low

    @property
    def low_bid(self):
        return self.original['lowBid']

    @property
    def low_ask(self):
        return self.original['lowAsk']

    @property
    def volume(self):
        return self.original['volume']

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