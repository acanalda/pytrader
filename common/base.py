import logging
from common.instruments import Instrument
import random
import string
from pymongo import MongoClient
from datetime import datetime
import settings

class Engine(object):

    def __init__(self, period, start_date, end_date):
        self._logger = logging.getLogger('engine')
        self._instruments = {}
        self._win_orders = self._lose_orders = 0
        self._db = None

        self.createDbConnection()
        self.initIntervals(period, start_date, end_date)

    def initIntervals(self, period, start_date, end_date):
        self._period = period
        self._start_date = start_date
        self._end_date = end_date

    def initAccount(self, usr, pwd, acc_id, name, balance, leverage, currency):
        self._account = Account(usr, pwd)
        self.account.updateAccountData({
            "accountId" : acc_id,
            "accountName" : name,
            "balance" : balance,
            "marginRate" : 1 / leverage,
            "accountCurrency" : currency
        })

    def createDbConnection(self):
        if not self.db:
            self._db = MongoClient(settings.DB_URL)

    def getInstrumentCollection(self, instrument):
        collection = self.db[settings.DB_NAME][instrument.code + '_' + instrument.period.code]
        collection.ensure_index('time', unique = True)
        return collection

    def registerInstrument(self, instrument):
        instrument._period = self.period
        self.instruments[instrument.code] = instrument

    def loadData(self):
        self.logger.info('Loading data: From %s To %s ...' % (self.start_date, self.end_date))
        for instrument in self.instruments.itervalues():
            self.loadInstrument(instrument)
        self.logger.info('Data loaded')

    def loadInstrument(self, instrument):
        instrument_collection = self.getInstrumentCollection(instrument)

        # load the DB candles
        db_candles = [candle for candle in instrument_collection \
            .find({"time": {"$gte": self.start_date, "$lte": self.end_date}}) \
            .sort('time', 1)]

        # load the DB canldes
        instrument.loadCandles(db_candles)

        # start the start date to download the broker's candles
        if len(db_candles) > 0:
            self._start_date = db_candles[-1]['time'] + self.period.toTimeDelta()

        candles = instrument.getBrokerCandles(self.start_date, self.end_date)
        self.logger.info('%s: %i new candles received from the broker' % (instrument.code, len(candles)))

        # Insert new candles to db
        for candle in candles:
            candle['time'] = datetime.strptime(candle['time'],'%Y-%m-%dT%H:%M:%S.%fZ')
            instrument_collection.insert(candle)

        # Insert new candles to instrument
        instrument.loadCandles(candles)

    def runStrategy(self, strategy, backtest):
        self._strategy = strategy
        self._backetest = backtest

        # Get the number of bars of any of the instruments
        historic_bars_count = len(self.instruments.itervalues().next().bars)

        # Inits the strategy indicators and support data
        strategy.start(self)

        # Run the system for all historic data
        for i in xrange(0, historic_bars_count):
            # Update the account data regarding open positions and last bar
            update_result = self.account.update(self.instruments, i)
            self._win_orders += update_result[0]
            self._lose_orders += update_result[1]

            # Update all instrument's indicators with the new bar
            for instrument in self.instruments.itervalues():
                strategy.newBar(instrument, i)

            # Run strategy decision algorithm
            strategy.execute(self, self.instruments, i)

        if backtest:
            strategy.end(self)
        else:
            raise NotImplementedError("Live mode not implemented yet")

    def createOrder(self, order):
        self.logger.info('%s %s %s' % (order.side, order.units, order.entry_price))
        self.account.orders[order.order_id] = order

    def closeOrder(self, order):
        del self.account.orders[order.order_id]

    def existsOrder(self, order):
        for o in self.account.orders.itervalues():
            if order.getCode() == o.getCode():
                return True
        return False

    def existsOppositeOrder(self, order):
        for o in self.account.orders.itervalues():
                if order.getOppositeCode() == o.getCode():
                    return True
        return False

    def convertAmountToAccountCcy(self, ref_currency, amount, cur_index):
        convert_factor = 1

        if ref_currency.code != self.account.account_currency.code:
            instrument_code_1 = Instrument.getCode(ref_currency, self.account.account_currency)
            instrument_code_2 = Instrument.getCode(self.account.account_currency, ref_currency)

            # Account currency is sold
            if instrument_code_1 in self.instruments:
                convert_instrument = self.instruments[instrument_code_1]
                convert_factor = convert_instrument.getBar(cur_index).close
            # Account currency is bought
            else:
                convert_instrument = self.instruments[instrument_code_2]
                convert_factor = 1 / convert_instrument.getBar(cur_index).close

        return convert_factor * amount

    def printResults(self):
        print  ('-------------------------- RESULTS -------------------------\n' + \
                'Acc Id: %s \n' % self.account.account_id + \
                'Acc Name: %s \n' % self.account.account_name + \
                'Strategy: %s \n' % self.strategy.name + \
                'Period: %s \n' % self.period + \
                'Start: %s \n' % self.start_date + \
                'End: %s \n' % self.end_date + \
                'Initial Balance: %s %s\n' % (self.account.inital_balance, self.account.account_currency.code)  + \
                'Current Balance: %s %s\n' % (self.account.balance, self.account.account_currency.code)  + \
                'Margin: %s \n' % self.account.margin_rate + \
                'Realized PL: %s %s\n' % (self.account.realized_pl, self.account.account_currency.code) + \
                'Unrealized PL: %s %s\n' % (self.account.unrealized_pl, self.account.account_currency.code) + \
                'Margin Used: %s \n' % self.account.margin_used + \
                'Margin Available: %s \n' % self.account.margin_avail + \
                'Current open orders: %s \n' % self.account.getNumOpenOrders() + \
                'Orders cost: %s %s \n' % (self.account.open_orders_cost, self.account.account_currency.code)  + \
                'Win operations: %s \n' % self.win_orders + \
                'Lose operations: %s \n' % self.lose_orders + \
                'Performance: %s %s \n' % (self.account.getPerformance(), '%') + \
                '------------------------- END RESULTS-----------------------'
                )
    # -------------------------------- properties -------------------

    @property
    def logger(self):
        return self._logger

    @property
    def account(self):
        return self._account

    @property
    def strategy(self):
        return self._strategy

    @property
    def backtest(self):
        return self._backtest

    @property
    def period(self):
        return self._period

    @property
    def start_date(self):
        return self._start_date

    @property
    def end_date(self):
        return self._end_date

    @property
    def instruments(self):
        return self._instruments

    @property
    def win_orders(self):
        return self._win_orders

    @property
    def lose_orders(self):
        return self._lose_orders

    @property
    def db(self):
        return self._db

""" ------------------- ACCOUNT ------------------- """
class Account(object):

    def __init__(self, usr, pwd):
        self._usr = usr
        self._pwd = pwd
        self._orders = {}
        self._inital_balance = None

    def updateAccountData(self, account_settings):
        self._account_id = account_settings['accountId']
        self._account_name = account_settings['accountName']
        self._balance = account_settings['balance']
        self._account_currency = account_settings['accountCurrency']
        self._margin_rate = account_settings['marginRate']

        # Computed attributes
        self._unrealized_pl = account_settings['unrealizedPl'] if 'unrealizedPl' in account_settings else 0
        self._realized_pl = account_settings['realizedPl'] if 'realizedPl' in account_settings else 0
        self._margin_used = account_settings['marginUsed'] if 'marginUsed' in account_settings else 0
        self._margin_avail = account_settings['marginAvail'] if 'marginAvail' in account_settings else 0
        self._open_trades = account_settings['openTrades'] if 'openTrades' in account_settings else 0
        self._open_orders = account_settings['openOrders'] if 'openOrders' in account_settings else 0

        if self.inital_balance is None:
            self._inital_balance = self.balance

    def update(self, instruments, index):
        aux_unrealized_pl = 0
        aux_margin_used = 0
        closed_wins = closed_loses = 0

        # update all the open orders
        for k in self.orders.keys():
            order = self.orders[k]
            order.update(index)
            if order.closed:
                self._realized_pl += order.profit # TODO: Broker spread
                self._balance += order.profit   # TODO: Broker spread
                if order.profit > 0:
                    closed_wins += 1
                elif order.profit < 0:
                    closed_loses += 1

                del self.orders[k]
            else:
                aux_unrealized_pl += order.profit
                aux_margin_used += order.cost * self.margin_rate

        self._unrealized_pl = aux_unrealized_pl
        self._margin_used = aux_margin_used
        self._margin_avail = self.balance - aux_margin_used

        return (closed_wins, closed_loses)

    def getPerformance(self):
        return ((self.balance - self.inital_balance) / self.inital_balance) * 100

    def getNumOpenOrders(self):
        return len(self.orders.keys())

    # -------------------------------- properties -------------------

    @property
    def account_id(self):
        return self._account_id

    @property
    def account_name(self):
        return self._account_name

    @property
    def balance(self):
        return self._balance

    @property
    def account_currency(self):
        return self._account_currency

    @property
    def margin_rate(self):
        return self._margin_rate

    @property
    def unrealized_pl(self):
        return self._unrealized_pl

    @property
    def realized_pl(self):
        return self._realized_pl

    @property
    def margin_used(self):
        return self._margin_used

    @property
    def margin_avail(self):
        return self._margin_avail

    @property
    def open_trades(self):
        return self._open_trades

    @property
    def open_orders(self):
        return self._open_orders

    @property
    def inital_balance(self):
        return self._inital_balance

    @property
    def orders(self):
        return self._orders

    @property
    def open_orders_cost(self):
        cost = 0
        for order in self.orders.values():
            cost += order.cost
        return cost


""" ------------------- ORDER ------------------- """
class Order(object):
    BUY = 'buy'
    SELL = 'sell'
    TYPE_MARKET = 'market'

    def __init__(self, engine, instrument, cur_index, units, side, take_profit_pips, stop_loss_pips):
        self._logger = logging.getLogger('order')

        self._order_id = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(4))
        self._engine = engine
        self._instrument = instrument
        self._units = units
        self._side = side
        self._take_profit_pips = take_profit_pips
        self._stop_loss_pips = stop_loss_pips
        self._entry_price = instrument.getBar(cur_index).close
        self._profit = 0
        self._closed = False

        # compute the cost of this position in Account currency
        cur_price = self.instrument.getBar(cur_index).close
        if self.side == Order.BUY:
            amount = self.units * cur_price
            self._cost = self.engine.convertAmountToAccountCcy(self.instrument.primary_ccy, amount, cur_index)
        else:
            amount = self.units * 1 / cur_price
            self._cost = self.engine.convertAmountToAccountCcy(self.instrument.secondary_ccy, amount, cur_index)

        # compute take profit and stop loss prices
        take_profit_inc = self.take_profit_pips * (instrument.pip_value * self.entry_price)
        stop_loss_inc = self.stop_loss_pips * (instrument.pip_value * self.entry_price)
        if side == Order.BUY:
            self._take_profit = self.entry_price + take_profit_inc
            self._stop_loss = self.entry_price - stop_loss_inc
        else:
            self._take_profit = self.entry_price - take_profit_inc
            self._stop_loss = self.entry_price + stop_loss_inc

    def getCode(self):
        return '%s_%s' % (self.instrument, self.side)

    def getOppositeCode(self):
        return '%s_%s' % (self.instrument, Order.BUY if self.side == Order.SELL else Order.SELL)

    def update(self, cur_index):
        cur_bar = self.instrument.getBar(cur_index)
        close_now = False
        ref_price = cur_bar.close

        # Update the profit
        if self.side == Order.BUY:
            # Check if we have to close the operation
            if cur_bar.high > self.take_profit:
                if not(cur_bar.low < self.stop_loss):
                    ref_price = self.take_profit
                    close_now = True
                else:
                    pass#print('LOW PRECISSION')
            elif cur_bar.low < self.stop_loss:
                if not (cur_bar.high > self.take_profit):
                    ref_price = self.stop_loss
                    close_now = True
                else:
                    pass#print('LOW PRECISSION')

            profit_price = self.units * (ref_price - self.entry_price)
            profit_currency = self.instrument.secondary_ccy
        else:
            # Check if we have to close the operation
            if cur_bar.low < self.take_profit:
                if not (cur_bar.high > self.stop_loss):
                    ref_price = self.take_profit
                    close_now = True
                else:
                    pass#print('LOW PRECISSION')
            elif cur_bar.high > self.stop_loss:
                if not (cur_bar.low < self.take_profit):
                    ref_price = self.stop_loss
                    close_now = True
                else:
                    pass#print('LOW PRECISSION')

            profit_price = self.units * (self.entry_price - ref_price)
            profit_currency = self.instrument.primary_ccy

        self._profit = self.engine.convertAmountToAccountCcy(profit_currency, profit_price, cur_index)
        if close_now:
            self.close(ref_price)

    def close(self, close_price):
        self.logger.info('CLOSE: %s units=%s entry=%s exit=%s profit=%f' %
                         (self.side, self.units, self.entry_price, close_price, self.profit))
        self._closed = True

    # -------------------------------- properties -------------------


    @property
    def order_id(self):
        return self._order_id

    @property
    def logger(self):
        return self._logger

    @property
    def engine(self):
        return self._engine

    @property
    def instrument(self):
        return self._instrument

    @property
    def cost(self):
        return self._cost

    @property
    def units(self):
        return self._units

    @property
    def side(self):
        return self._side

    @property
    def take_profit_pips(self):
        return self._take_profit_pips

    @property
    def stop_loss_pips(self):
        return self._stop_loss_pips

    @property
    def take_profit(self):
        return self._take_profit

    @property
    def stop_loss(self):
        return self._stop_loss

    @property
    def entry_price(self):
        return self._entry_price

    @property
    def profit(self):
        return self._profit

    @property
    def closed(self):
        return self._closed