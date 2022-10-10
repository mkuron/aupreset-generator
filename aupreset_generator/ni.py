import os
import sqlite3

from .aupreset import write


def convert_ni():
    src = "/Users/mkuron/Library/Application Support/Native Instruments/Massive/NIMassiveDatabase2_ul"
    destdir = "/Library/Audio/Presets/Native Instruments/Massive"
    magic = int('NiMa'.encode('ascii').hex(), base=16)

    if not os.path.exists(src):
        return False

    db = sqlite3.connect(f'file:{src}?mode=ro', uri=True)
    cur = db.cursor()
    q = cur.execute("""SELECT doc_name, DocPath, Bankname, KP_Type
                       FROM NIPresetMgrTable""")
    for row in q:
        nksf = {'NISI': {'vendor': 'Native Instruments', 'name': row[0]}, 'PLID': {'VST.magic': magic}}
        category = row[3][2:row[3].find('}')].replace('/', ' and ')
        if len(category) == 0:
            continue
        dest = os.path.join(destdir, row[2], category, row[0]) + '.aupreset'
        print(row, dest)
        with open(row[1], 'rb') as f:
            nksf['PCHK'] = f.read()

        if not os.path.exists(os.path.dirname(dest)):
            os.makedirs(os.path.dirname(dest))
        write(nksf, dest)


if __name__ == '__main__':
    convert_ni()
