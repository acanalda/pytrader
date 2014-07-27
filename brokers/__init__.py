class Broker:

    def getCandles(self, instrument, start_date, end_date, period):
        raise NotImplementedError("Should have implemented this")

    @property
    def name(self):
        return self._name

    @property
    def usr(self):
        return self._usr

    @property
    def pwd(self):
        return self._pwd

    @property
    def base_url(self):
        return self._base_url

