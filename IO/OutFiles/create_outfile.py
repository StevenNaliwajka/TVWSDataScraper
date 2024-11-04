from IO.OutFiles.OutfileTypes.Browser.browser import Browser
from IO.OutFiles.OutfileTypes.LocalDB.localdb import LocalDB
from IO.OutFiles.OutfileTypes.TXT.txt import TXT


def create_outfile(name, outfile_type, location):
    outfile_type = outfile_type.lower()
    outfile_switcher = {
        "browser": Browser(name, 'browser', location),
        "localdb": LocalDB(name, 'localdb', location),
        "txt": TXT(name, 'txt', location)
    }

    new_outfile = outfile_switcher.get(outfile_type)

    return new_outfile