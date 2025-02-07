from CodeBase.IO.OutFiles.OutfileTypes.outfile_parent import OutfileParent


class Browser(OutfileParent):
    def __init__(self, name, outfile_type, location, base_station, child_radio_list):
        super().__init__(name, outfile_type, location, base_station, child_radio_list)

        ## NOT SUPPORTED

    def write_to_outfile(self, data_to_write):
        pass
