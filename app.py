import logging
from datetime import datetime
from common.base import Engine
from common.instruments import EURGBP, EURAUD, EURUSD, EURCAD, EURCHF, EURJPY, GBPUSD, GBPJPY, GBPCAD, GBPCHF, GBPAUD,\
    AUDUSD, AUDCHF, AUDCAD, AUDJPY, USDCAD, USDCHF, USDJPY, CADJPY, CADCHF, CHFJPY
from common.instruments import EUR
from common import periods
from strategies.basicEma import BasicEma
import settings

BACKTEST = True
BEGIN_DATE = datetime(2014, 3, 1, 0, 0)
END_DATE = datetime.utcnow()
LEVERAGE = 20.0
PERIOD = periods.H1()
STRATEGY = BasicEma()

def main():
    logging.basicConfig(format = '%(levelname)s %(name)s %(asctime)s %(message)s', level = logging.DEBUG)

    # Load first max precission date from the broker
    #if BACKTEST:
    #    loadMaxPrecissionData(datetime(2014, 7, 21, 0, 0), END_DATE)

    # Create the engine
    engine = Engine(PERIOD, BEGIN_DATE, END_DATE)

    # Setup engine
    engine.initAccount(
                       broker_name = 'oanda',
                       usr = settings.BROKER_USR,
                       pwd = settings.BROKER_PWD,
                       acc_id = 1,
                       acc_name = 'paper',
                       balance = 10000,
                       leverage = LEVERAGE,
                       currency = EUR()
                       )

    # Register all the instruments used by the system
    registerInstruments(engine)

    engine.loadData()
    engine.runStrategy(strategy = STRATEGY, backtest = BACKTEST)
    engine.printResults()

def registerInstruments(engine):
    engine.registerInstrument(EURUSD())
    return

    # EUR
    engine.registerInstrument(EURGBP())
    engine.registerInstrument(EURAUD())
    engine.registerInstrument(EURUSD())
    engine.registerInstrument(EURCAD())
    engine.registerInstrument(EURCHF())
    engine.registerInstrument(EURJPY())
    # GBP
    engine.registerInstrument(GBPUSD())
    engine.registerInstrument(GBPAUD())
    engine.registerInstrument(GBPCHF())
    engine.registerInstrument(GBPCAD())
    engine.registerInstrument(GBPJPY())
    # AUD
    engine.registerInstrument(AUDUSD())
    engine.registerInstrument(AUDCHF())
    engine.registerInstrument(AUDCAD())
    engine.registerInstrument(AUDJPY())
    # USD
    engine.registerInstrument(USDCAD())
    engine.registerInstrument(USDCHF())
    engine.registerInstrument(USDJPY())
    # CAD
    engine.registerInstrument(CADCHF())
    engine.registerInstrument(CADJPY())
    # CHF
    engine.registerInstrument(CHFJPY())

def loadMaxPrecissionData(begin_date, final_date):
    engine = Engine(periods.S5(), begin_date, final_date)
    registerInstruments(engine)
    inc = periods.H4().toTimeDelta()
    end_date = begin_date + inc
    while end_date < final_date:
        engine.initIntervals(periods.S5(), begin_date, end_date)
        engine.loadData()
        begin_date = end_date
        end_date = end_date + inc

if __name__ == '__main__':
    main()
