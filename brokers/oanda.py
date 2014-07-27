from brokers import Broker
from rfc3339 import rfc3339
import json
import urllib2
import urllib

class Oanda(Broker):

    def __init__(self, usr, pwd):
        self._name = 'oanda'
        self._base_url = 'http://api-sandbox.oanda.com/v1'
        self._usr = usr
        self._pwd = pwd

    # -------------------------------- properties -------------------

    def getCandles(self, instrument, start_date, end_date, period):
        url = self.base_url + '/candles'
        start_rfc = rfc3339(start_date, utc = True, use_system_timezone = False)
        end_rfc = rfc3339(end_date, utc = True, use_system_timezone = False)
        values = {
          'instrument': instrument.code,
          'granularity': period.code,
          'candleFormat': 'bidask',
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