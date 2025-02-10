def change_setting(base_station, setting_type, setting_tag, value, unit, read_method):
    current_value = f"{base_station.__dict__[setting_type]} {unit}"

    if isinstance(value, int):
        if unit == "CH":
            new_value = f"{unit} {value}"
        else:
            new_value = f"{value} {unit}"
        change_generic_setting(setting_tag, new_value, current_value)
    if isinstance(value, float):
        value = clean_decimal(value)
        if unit == "CH":
            new_value = f"{unit} {value}"
        else:
            new_value = f"{value} {unit}"
        change_generic_setting(setting_tag, new_value, current_value)
    elif value.lower() == "up":
        change_generic_setting(setting_tag, "up", current_value)
    elif value.lower() == "down":
        change_generic_setting(setting_tag, "down", current_value)

    # Call the corresponding read method
    read_method()
