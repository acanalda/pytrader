from strategies import Strategy
from indicators.EMA import EMA
from indicators.SMA import SMA
from indicators.ATR import ATR
from common.instruments import Bar
import logging


class CcyBasket(Strategy):
    STRATEGY_NAME = 'CcyBasket'

    def __init__(self):
        self._logger = logging.getLogger('basket')

    def start(self, engine):
        self.logger.info('Ccy starts')
        self._name = CcyBasket.STRATEGY_NAME

        # setup the indicators
        self._sma = SMA(5, Bar.CLOSE)
        self._ema = EMA(5, Bar.CLOSE)
        self._atr = ATR(5, Bar.CLOSE)

    def newBar(self, instrument, cur_index):
        #print ('newBar: %s %s %f' % (instrument.bars[cur_index].time,
        #                                instrument.code,
        #                                getattr(instrument.bars[cur_index], Bar.CLOSE)))

        # update indicators
        self.atr.update(instrument, cur_index)
        self.ema.update(instrument, cur_index)
        self.sma.update(instrument, cur_index)

    def execute(self, engine, instruments, cur_index):
        self.logger.info('Ccy decide')

    def end(self, engine):
        self.logger.info('Ccy ends')
        pass
        #print ('Ccy onStop')
        #print ('ATR:')
        #print(self.atr.values)
        #print ('SMA:')
        #print(self.sma.values)
        #print ('EMA:')
        #print(self.ema.values)

    # -------------------------------- properties -------------------

    @property
    def logger(self):
        return self._logger

    @property
    def name(self):
        return self._name

    @property
    def atr(self):
        return self._atr

    @property
    def sma(self):
        return self._sma

    @property
    def ema(self):
        return self._ema