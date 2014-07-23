class Strategy:

    """Called on strategy start."""
    def start(self, engine):
        raise NotImplementedError("Should have implemented this")

    """Called on every bar of every instrument that client is subscribed on."""
    def newBar(self, instrument, cur_index):
        raise NotImplementedError("Should have implemented this")

    """Called on after all indicators have been updated for this bar's index"""
    def execute(self, engine, instruments, cur_index):
        raise NotImplementedError("Should have implemented this")

    """Called on strategy stop."""
    def end(self, engine):
        raise NotImplementedError("Should have implemented this")