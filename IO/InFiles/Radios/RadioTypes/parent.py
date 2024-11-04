from IO.InFiles.Radios.radio_parent import RadioParent


class Parent(RadioParent):
    def __init__(self, name, location):
        super().__init__(name, location)
        self.rx_gain = None
        self.channel = None
        self.freq = None
        self.noise = None
        self.tx_power = None
        self.bandwidth = None

