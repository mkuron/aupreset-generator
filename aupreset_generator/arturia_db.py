from collections import defaultdict
import os
import plistlib
import re
import sqlite3

from .aupreset import write


def convert_arturia_db():
    srcdir = "/Library/Arturia/Presets"
    src = os.path.join(srcdir, "db.db3")
    destdir = "/Library/Audio/Presets/Arturia"
    plugindir = "/Library/Audio/Plug-Ins/Components"

    if not os.path.exists(srcdir):
        return False

    db = sqlite3.connect(f'file:{src}?mode=ro', uri=True)
    cur = db.cursor()
    q = cur.execute("""SELECT DISTINCT Instruments.name, Types_V2.name, Subtypes_V2.name
                       FROM Preset_Id
                       INNER JOIN Instruments ON instrument_key = Instruments.key_id
                       INNER JOIN Types_V2 ON type_v2 = Types_V2.key_id
                       INNER JOIN Subtypes_V2 ON subtype_v2 = Subtypes_V2.key_id
                       WHERE Types_V2.name NOT LIKE 'Template%'""")
    types = defaultdict(set)
    subtypes = defaultdict(set)
    for row in q:
        types[row[0]].add(row[1])
        subtypes[row[0]].add(row[2])
    q = cur.execute("""SELECT Instruments.name, Types_V2.name, Packs.name, Preset_Id.name, file_path, comment, Subtypes_V2.name
                       FROM Preset_Id
                       INNER JOIN Instruments ON instrument_key = Instruments.key_id
                       INNER JOIN Types_V2 ON type_v2 = Types_V2.key_id
                       INNER JOIN Subtypes_V2 ON subtype_v2 = Subtypes_V2.key_id
                       INNER JOIN Packs ON pack = Packs.key_id
                       WHERE file_path NOT LIKE '%/User/Playlist/%'
                       AND Types_V2.name NOT LIKE 'Template%'""")
    for row in q:
        instrument = os.path.relpath(row[4], start=srcdir).split(os.sep)[0]
        plugin = os.path.join(plugindir, f'{instrument}.component', 'Contents', 'Info.plist')
        if not os.path.exists(plugin):
            continue
        with open(plugin, 'rb') as f:
            magic = int(plistlib.load(f)['AudioComponents'][0]['subtype'].encode('ascii').hex(), base=16)
        category = row[1].replace(' & ', ' and ') if len(types[row[0]]) > 2 else row[6]
        category = os.path.join(row[2], category) if len(subtypes[row[0]]) >= 2 else row[2]
        name = row[3]
        if row[2] == 'Vintage Factory' and row[5]:
            m = re.search("Preset ([0-9]+) from the original factory library", row[5])
            if m:
                name = f'{m.group(1)} {name}'
        nksf = {'NISI': {'vendor': 'Arturia', 'name': name}, 'PLID': {'VST.magic': magic}}
        dest = os.path.join(destdir, instrument, category, name) + '.aupreset'
        print(row, dest)
        with open(row[4], 'rb') as f:
            nksf['PCHK'] = f.read()

        if not os.path.exists(os.path.dirname(dest)):
            os.makedirs(os.path.dirname(dest))
        write(nksf, dest)

        # After switching presets inside the AudioUnit, loading a preset from the DAW controls has no further effect.
        # This is not restricted to generated presets, it also happens when saving/restoring.


if __name__ == '__main__':
    convert_arturia_db()
