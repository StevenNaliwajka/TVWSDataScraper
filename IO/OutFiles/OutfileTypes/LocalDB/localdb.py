from IO.OutFiles.OutfileTypes.outfile_parent import OutfileParent


class LocalDB(OutfileParent):
    def __init__(self, name, outfile_type, location):
        super().__init__(name, outfile_type, location)

        ## NOT SUPPORTED

    def write_to_outfile(self, data_to_write):
        pass
