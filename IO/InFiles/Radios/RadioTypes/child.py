from IO.InFiles.Radios.radio_parent import RadioParent


class Child(RadioParent):
    def __init__(self, name, base_antenna_angle, this_antenna_angle, h_distance, v_distance,
                 special_char_name, special_char_value):
        # Child radio type, used as a "register" to store data, Constantly pulled from and pushed too.

        super().__init__(name)
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

    def push_data(self, key, value):
        # Should only be used for the 'register' values
        key = "_"+key
        if hasattr(self, key):
            attr = getattr(self, key)
            if isinstance(attr, list):
                attr.append(value)
            else:
                setattr(self, key, value)
        else:
            raise ValueError("Key not in Child Radio object.")

    def pull_data(self, key):
        key = "_" + key
        # Should only be used for the 'register' values
        # Stores data in lists, averages the values stored.
        if hasattr(self, key):
            value = getattr(self, key)
            avg = sum(value) / len(value)
            if isinstance(value, list):
                setattr(self, key, [])
            else:
                setattr(self, key, None)
            return avg
        else:
            raise ValueError("Key not in Child Radio object.")

