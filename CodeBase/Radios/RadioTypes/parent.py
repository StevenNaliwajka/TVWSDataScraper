from CodeBase.Radios.radio_parent import RadioParent


class Parent(RadioParent):
    def __init__(self, name, ip):
        # The base station, currently for all intents and purposes, there should only be one.
        super().__init__(name, ip)

        # 'constants', will be changed in the webGUI to get changes data.
        # Currently there are on avg 4 channels avail.
        self.channel = None
        self.freq = None
        self.noise = None

        # 19 tx power avail
        self.tx_power = None

        # 45 Rx gain avail
        self.rx_gain = None

        # 4 Channel bandwidth avail
        self.bandwidth = None

        self.temp = None
        self.uptime_value = None
        self.base_free_mem = None
        self.location = None