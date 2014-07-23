from indicators import Indicator
import numpy as np

class EMA(Indicator):
    def __init__(self, window, bar_value = 'close'):
        super(EMA, self).__init__()

        self._window = window
        self._bar_value = bar_value

        # setup the ema weights
        self._weights = np.exp(np.linspace(-1., 0., window))
        self._weights /= self.weights.sum()

    def update(self, instrument, cur_index):
        # Check if we got enough bars
        if cur_index >= self.window:
            # get the las 'window' items
            dataset = instrument.bars[cur_index - self.window:cur_index]
            # parse the bars value
            dataset = [getattr(bar, self.bar_value) for bar in dataset]
            last_value = self.compute(dataset, self._window)
            self._values.append(last_value)
        else:
            self._values.append(None)

    def compute(self, values, window):
        # Here, we will just allow the default since it is an EMA
        emas =  np.convolve(values, self.weights)[:len(values)]
        #again, as a numpy array.
        emas[:window - 1] = emas[window - 1]
        return emas[-1]

    # ---------------------------------- properties -----------------------------
    @property
    def window(self):
        return self._window

    @property
    def bar_value(self):
        return self._bar_value

    @property
    def weights(self):
        return self._weights