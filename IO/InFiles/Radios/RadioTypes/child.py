from IO.InFiles.Radios.radio_parent import RadioParent


class Child(RadioParent):
    def __init__(self, name, location, base_antenna_angle, this_antenna_angle, h_distance, v_distance,
                 special_char_name, special_char_value):
        super().__init__(name, location)
        self.base_antenna_angle = base_antenna_angle
        self.this_antenna_angle = this_antenna_angle
        self.h_distance = h_distance
        self.v_distance = v_distance
        # Special Characteristic
        self.special_char_name = special_char_name
        self.special_char_value = special_char_value

        self.down_s0 = []
        self.down_s1 = []
        self.down_rssi = []
        self.down_noise_floor = []
        self.down_snr = []
        self.tx_power = []
        self.up_s0 = []
        self.up_s1 = []
        self.up_rssi = []
        self.up_noise_floor = []
        self.up_snr = []
        self.ping_time_avg = []

