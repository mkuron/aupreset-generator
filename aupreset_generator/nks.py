from chunk import Chunk

import msgpack


def read(filename):
    data = {}
    with open(filename, "rb") as f:
        f.seek(12)
        while True:
            try:
                chunk = Chunk(f, bigendian=False)
            except EOFError:
                break
            t = chunk.getname().decode('ascii')
            d = chunk.read()[4:]
            if t in ['NISI', 'NICA', 'PLID']:
                d = msgpack.unpackb(d)
            data[t] = d
    return data
