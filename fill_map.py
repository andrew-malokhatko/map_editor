import struct

with open("map.bin", "wb") as f:
    for i in range(20):
        for k in range(20):
            if i % 2 == 0:
                data = struct.pack("hhb", i, k, 0)
            else:
                data = struct.pack("hhb", i, k, 1)
            f.write(data)
