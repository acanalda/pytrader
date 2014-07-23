import json
import urllib2
import urllib
from common.libs.rfc3339 import rfc3339
import settings

class Instrument(object):
    def __init__(self, primary_ccy, secondary_ccy, pip_value, pip_scale):
        self._period = None
        self._bars = []

        self._primary_ccy = primary_ccy
        self._secondary_ccy = secondary_ccy
        self._pip_value = pip_value
        self._pip_scale = pip_scale

    def getBrokerCandles(self, start_date, end_date):
        url = settings.BASE_URL + '/candles'
        start_rfc = rfc3339(start_date, utc = True, use_system_timezone = False)
        end_rfc = rfc3339(end_date, utc = True, use_system_timezone = False)
        values = {
          'instrument': self.code,
          'granularity': self.period.code,
          'candleFormat': settings.CANDLE_FORMAT,
          'start': start_rfc,
          'end': end_rfc,
          'includeFirst': 'true'
        }
        url_values = urllib.urlencode(values)
        complete_url = '%s?%s' % (url, url_values)
        req = urllib2.Request(complete_url)
        try:
            response = urllib2.urlopen(req)
            json_str = response.read()
        except:
            json_str = '{"candles": []}'
            pass

        if json_str:
            json_obj = json.loads(json_str)
            return json_obj['candles']
        return[]

    def loadCandles(self, candles):
        for candle in candles:
            bar = Bar(candle)
            #print ('%s - %s - %f' % (self.code, bar.time, bar.open_bid))
            self._bars.append(bar)

    def getBar(self, index):
        return self.bars[index]

    @staticmethod
    def getCode(ccy1, ccy2):
        return '%s_%s' % (ccy1.code, ccy2.code)

    # -------------------------------- properties -------------------

    @property
    def period(self):
        return self._period

    @property
    def bars(self):
        return self._bars

    @property
    def primary_ccy(self):
        return self._primary_ccy

    @property
    def secondary_ccy(self):
        return self._secondary_ccy

    @property
    def pip_value(self):
        return self._pip_value

    @property
    def pip_scale(self):
        return self._pip_scale

    @property
    def code(self):
        return Instrument.getCode(self.primary_ccy, self.secondary_ccy)

""" EUR """
class EURGBP(Instrument):
    def __init__(self): super(EURGBP, self).__init__(EUR(), GBP(), 0.0001, 4)
class EURAUD(Instrument):
    def __init__(self): super(EURAUD, self).__init__(EUR(), AUD(), 0.0001, 4)
class EURUSD(Instrument):
    def __init__(self): super(EURUSD, self).__init__(EUR(), USD(), 0.0001, 4)
class EURCAD(Instrument):
    def __init__(self): super(EURCAD, self).__init__(EUR(), CAD(), 0.0001, 4)
class EURCHF(Instrument):
    def __init__(self): super(EURCHF, self).__init__(EUR(), CHF(), 0.0001, 4)
class EURJPY(Instrument):
    def __init__(self): super(EURJPY, self).__init__(EUR(), JPY(), 0.01, 2)

""" GBP """
class GBPUSD(Instrument):
    def __init__(self): super(GBPUSD, self).__init__(GBP(), USD(), 0.0001, 4)
class GBPAUD(Instrument):
    def __init__(self): super(GBPAUD, self).__init__(GBP(), AUD(), 0.0001, 4)
class GBPCHF(Instrument):
    def __init__(self): super(GBPCHF, self).__init__(GBP(), CHF(), 0.0001, 4)
class GBPCAD(Instrument):
    def __init__(self): super(GBPCAD, self).__init__(GBP(), CAD(), 0.0001, 4)
class GBPJPY(Instrument):
    def __init__(self): super(GBPJPY, self).__init__(GBP(), JPY(), 0.01, 2)

""" AUD """
class AUDUSD(Instrument):
    def __init__(self): super(AUDUSD, self).__init__(AUD(), USD(), 0.0001, 4)
class AUDCHF(Instrument):
    def __init__(self): super(AUDCHF, self).__init__(AUD(), CHF(), 0.0001, 4)
class AUDCAD(Instrument):
    def __init__(self): super(AUDCAD, self).__init__(AUD(), CAD(), 0.0001, 4)
class AUDJPY(Instrument):
    def __init__(self): super(AUDJPY, self).__init__(AUD(), JPY(), 0.01, 2)

""" USD """
class USDCAD(Instrument):
    def __init__(self): super(USDCAD, self).__init__(USD(), CAD(), 0.0001, 4)

class USDCHF(Instrument):
    def __init__(self): super(USDCHF, self).__init__(USD(), CHF(), 0.0001, 4)

class USDJPY(Instrument):
    def __init__(self): super(USDJPY, self).__init__(USD(), JPY(), 0.01, 2)

""" CAD """
class CADCHF(Instrument):
    def __init__(self): super(CADCHF, self).__init__(CAD(), CHF(), 0.0001, 4)

class CADJPY(Instrument):
    def __init__(self): super(CADJPY, self).__init__(CAD(), JPY(), 0.01, 2)

""" CHF """
class CHFJPY(Instrument):
    def __init__(self): super(CHFJPY, self).__init__(CHF(), JPY(), 0.01, 2)


""" ------------------- CURRENCY ------------------- """
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