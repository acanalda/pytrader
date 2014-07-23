from indicators import Indicator
import numpy as np

class SMA(Indicator):
    def __init__(self, window, bar_value = 'close'):
        super(SMA, self).__init__()

        self._window = window
        self._bar_value = bar_value

        # setup the ema weights
        self._weights = np.repeat(1.0, window)/window

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
        #including valid will REQUIRE there to be enough datapoints.
        #for example, if you take out valid, it will start @ point one,
        #not having any prior points, so itll be 1+0+0 = 1 /3 = .3333
        smas = np.convolve(values, self.weights, 'valid')
        return smas[-1]

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