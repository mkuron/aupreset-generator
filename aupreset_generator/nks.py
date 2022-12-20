import msgpack


def read(filename):
    data = {}
    with open(filename, "rb") as f:
        f.seek(12)
        while True:
            t = f.read(4).decode('ascii')
            s = int.from_bytes(f.read(4), 'little')
            d = f.read(s)[4:]
            if len(d) == 0:
                break
            if t in ['NISI', 'NICA', 'PLID']:
                data[t] = msgpack.unpackb(d)
            else:
                data[t] = d
            if s % 2 == 1:
                f.seek(1, 1)
        print(data.keys())
        return data
