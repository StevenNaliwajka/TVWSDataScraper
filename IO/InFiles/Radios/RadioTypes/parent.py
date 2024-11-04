from IO.InFiles.Radios.radio_parent import RadioParent


class Parent(RadioParent):
    def __init__(self, name):
        # The base station, currently for all intents and purposes, there should only be one.
        super().__init__(name)

        # 'constatnts', will be changed in the webGUI to get changes data.
        self.rx_gain = None
        self.channel = None
        self.freq = None
        self.noise = None
        self.tx_power = None
        self.bandwidth = None

