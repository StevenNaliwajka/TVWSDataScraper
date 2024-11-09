from IO.InFiles.Radios.radio_parent import RadioParent


class Parent(RadioParent):
    def __init__(self, name, cycle_channel, cycle_tx_power, cycle_rx_gain, cycle_bandwidth):
        # The base station, currently for all intents and purposes, there should only be one.
        super().__init__(name)

        # 'constants', will be changed in the webGUI to get changes data.
        self.cycle_channel = cycle_channel
        # Currently there are on avg 4 channels avail.
        self.channel = None
        self.freq = None
        self.noise = None

        self.cycle_tx_power = cycle_tx_power
        # 19 tx power avail
        self.tx_power = None

        self.cycle_rx_gain = cycle_rx_gain
        # 45 Rx gain avail
        self.rx_gain = None

        self.cycle_bandwidth = cycle_bandwidth
        # 4 Channel bandwidth avail
        self.bandwidth = None

        self.temp = None

