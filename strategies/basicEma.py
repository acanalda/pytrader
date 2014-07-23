from strategies import Strategy
from indicators.EMA import EMA
from indicators.ATR import ATR
from common.instruments import Bar
from common.base import Order
import logging

class BasicEma(Strategy):
    STRATEGY_NAME = 'BasicEma'

    def __init__(self):
        self._logger = logging.getLogger('basicEma')

    def start(self, engine):
        self.logger.info('Starts')
        self._name = BasicEma.STRATEGY_NAME

        # setup the indicators
        self._ema_short = EMA(12, Bar.CLOSE) # 12
        self._ema_long = EMA(26, Bar.CLOSE) # 26
        self._atr = ATR(12, Bar.CLOSE)

    def newBar(self, instrument, cur_index):
        # update indicators
        self.ema_short.update(instrument, cur_index)
        self.ema_long.update(instrument, cur_index)
        self.atr.update(instrument, cur_index)

    def execute(self, engine, instruments, cur_index):
        atr = self.atr.getLast()
        if atr:
            # Go through all instruments
            for instrument in instruments.itervalues():
                order = None
                take_proffit = atr * 3
                stop_loss = atr * 1
                units = 100
                # crossing up
                if self.ema_short.crossUp(self.ema_long):
                    order = Order(engine, instrument, cur_index, units, Order.BUY, take_proffit, stop_loss)
                # crossing down
                elif self.ema_short.crossDown(self.ema_long):
                    order = Order(engine, instrument, cur_index, units, Order.SELL, take_proffit, stop_loss)

                # make sure theres no open orders with this instrument
                if order:# and not (engine.existsOrder(order) or engine.existsOppositeOrder(order)):
                    engine.createOrder(order)

    def end(self, engine):
        self.logger.info('Ends')
        pass

    # -------------------------------- properties -------------------

    @property
    def logger(self):
        return self._logger

    @property
    def name(self):
        return self._name

    @property
    def ema_short(self):
        return self._ema_short

    @property
    def ema_long(self):
        return self._ema_long

    @property
    def atr(self):
        return self._atr