from indicators import Indicator
import numpy as np

class ATR(Indicator):
    def __init__(self, window, bar_value = 'close', in_pips = True):
        super(ATR, self).__init__()

        self._window = window
        self._bar_value = bar_value
        self._in_pips = in_pips

        # setup the ema weights
        self._weights = np.exp(np.linspace(-1., 0., window))
        self._weights /= self.weights.sum()

    def update(self, instrument, cur_index):
        # Check if we got enough bars
        if cur_index >= self.window:
            # get the las 'window' items
            dataset = instrument.bars[cur_index - self.window:cur_index]
            # parse the bars value
            true_ranges = [self.TR(bar, instrument) for bar in dataset]
            last_value = self.compute(true_ranges, self._window)
            self._values.append(last_value)
        else:
            self._values.append(None)

    # applies exponential moving average
    def compute(self, values, window):
        # Here, we will just allow the default since it is an EMA
        emas =  np.convolve(values, self.weights)[:len(values)]
        #again, as a numpy array.
        emas[:window - 1] = emas[window - 1]
        return emas[-1]

    # computes the true range of a bar. Returns PIP's
    def TR(self, bar, instrument):
        x = bar.high - bar.low
        y = abs(bar.high - bar.volume)
        z = abs(bar.low - bar.volume)

        if y <= x >= z:
            tr = x
        elif x <= y >= z:
            tr = y
        elif x <= z >= y:
            tr = z

        if self.in_pips:
            return tr * instrument.pip_value
        else:
            return tr

    # ---------------------------------- properties -----------------------------
    @property
    def window(self):
        return self._window

    @property
    def bar_value(self):
        return self._bar_value

    @property
    def in_pips(self):
        return self._in_pips

    @property
    def weights(self):
        return self._weights