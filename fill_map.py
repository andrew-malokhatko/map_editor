import struct

with open("map.bin", "wb") as f:
    for i in range(20):
        for k in range(20):
            data = struct.pack("hhb", i, k, 0)
            f.write(data)
