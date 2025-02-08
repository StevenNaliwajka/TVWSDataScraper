from CodeBase.OutFiles.OutfileTypes.Browser.browser import Browser
from CodeBase.OutFiles.OutfileTypes.CSVFile.csv_file import CSVFile
from CodeBase.OutFiles.OutfileTypes.LocalDB.localdb import LocalDB


def create_outfile(name, outfile_type, location, base_station, child_radio_list):
    outfile_type = outfile_type.lower()
    outfile_switcher = {
        "browser": Browser(name, 'browser', location, base_station, child_radio_list),
        "localdb": LocalDB(name, 'localdb', location, base_station, child_radio_list),
        "csv": CSVFile(name, 'csv', location, base_station, child_radio_list)
    }

    new_outfile = outfile_switcher.get(outfile_type)
    return new_outfile
