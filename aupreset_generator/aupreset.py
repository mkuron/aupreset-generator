import plistlib


def write(nksf, filename):
    vendors = {
        'Arturia': ('Artu', 'Controller State'),  # 1098019957
        'Native Instruments': ('-NI-', 'vstdata'),
        'Waldorf': ('3E00', 'Processor State'),  # 860172336
    }
    manufacturer, field = vendors[nksf['NISI']['vendor']]
    plist = {
        field: nksf['PCHK'],
        'manufacturer': int(manufacturer.encode('ascii').hex(), base=16),
        'subtype': nksf['PLID']['VST.magic'],
        'type': int(b'aumu'.hex(), base=16),  # 1635085685
        'version': 0,
        'name': nksf['NISI']['name'],
    }
    with open(filename, 'wb') as f:
        plistlib.dump(plist, f, fmt=plistlib.FMT_XML)
