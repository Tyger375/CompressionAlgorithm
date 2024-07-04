class Bits:
    def __init__(self, bits, size: int):
        self.bits = bits
        self.size = size

    def __repr__(self):
        s = ""
        for i in range(self.size):
            s += bin((self.bits & (1 << i)) != 0)[-1]
        return s[::-1]


def unite(bits: list):
    full = "".join([str(bit) for bit in bits])
    size = len(full)
    return full + "0" * (8 - (size % 8))


def str_to_bits(s: str):
    val = 0
    for i, c in enumerate(s[::-1]):
        if c == '1':
            val += (1 << i)
    return Bits(val, len(s))


def str_to_bytes(s: str) -> bytearray:
    array = bytearray()
    #   256 128 64  32  16  8   4   2   1
    #   0   0   1   0   0   1   0   0   1
    #   1   0   0   0   0   1   1   0   1
    #   0   0   1   0   0   0   0   1   1
    #       0   1   1   0   0   1   1   0
    index = 0
    while index < len(s):
        part = s[index:index + 8]
        index += 8
        array.append(int(part, 2))
    return array
