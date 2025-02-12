from CodeBase.Radios.radio_parent import RadioParent


class Child(RadioParent):
    def __init__(self, name, base_antenna_angle, this_antenna_angle, h_distance, v_distance,
                 special_char_name, special_char_value, ip):
        # Child radio type, used as a "register" to store data, Constantly pulled from and pushed too.
        # print("Creating A radio pair")
        super().__init__(name, ip)
        # 'config data'
        self.base_antenna_angle = base_antenna_angle
        self.this_antenna_angle = this_antenna_angle
        self.h_distance = h_distance
        self.v_distance = v_distance
        # Special Characteristic
        self.special_char_name = special_char_name
        self.special_char_value = special_char_value

        # 'values to be read'
        self._down_s0 = []
        self._down_s1 = []
        self._down_rssi = []
        self._down_noise_floor = []
        self._down_snr = []
        self._tx_power = []
        self._up_s0 = []
        self._up_s1 = []
        self._up_rssi = []
        self._up_noise_floor = []
        self._up_snr = []
        self._ping_time_avg = []

        # String Data
        self.down_tx_mod = None
        self.down_rx_mod = None
        self.radio_temp = None
        self.radio_location = None
        self.radio_uptime = None
        self.radio_up_link_time = None
        self.up_rxmod = None
        self.up_rxpkt = None
        self.up_txmod = None
        self.up_txpkt = None

        # Added on run, the position in webgui of radio, 1,2,3,4...
        self.radio_count = None

    def push_data(self, key, value):
        # Should only be used for the 'register' values
        key = "_" + key
        if hasattr(self, key):
            attr = getattr(self, key)
            if isinstance(attr, list):
                attr.append(value)
            else:
                setattr(self, key, value)
        else:
            raise ValueError(f"(ChildRadio): Key \'{key}\' not in radio \'{self.name}\' object.")

    def pull_data(self, key):
        key = "_" + key
        # Should only be used for the 'register' values
        # Stores data in lists, averages the values stored.
        if hasattr(self, key):
            values = getattr(self, key)
            avg = sum(values) / len(values) if len(values) > 0 else 0
            if isinstance(values, list):
                setattr(self, key, [])
            else:
                setattr(self, key, None)
            return avg
        else:
            raise ValueError(f"(ChildRadio): Key \'{key}\' not in radio \'{self.name}\' object.")

