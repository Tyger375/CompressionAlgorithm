import numpy
from bitstring import Array
from progress.bar import Bar


MAP = {
    3: {
        1: 2,
        2: 1
    },
    2: {
        1: 1,
        2: 0
    },
    1: {
        1: 0,
        2: 0
    }
}


# 1 -> first type (2 chars similarity for octal)
# 2 -> second type (1 char similarity for octal)
def similar(s: str, string: str, t: int) -> tuple[int, str]:
    l = len(s)
    offset = MAP[l][t]
    if offset == 0:
        return -1, ""

    end = s[l - offset:l]
    start = s[0:offset]
    # print(other, end, string, start)
    if string.endswith(start):
        return 1, s[offset:]
    elif string.startswith(end):
        return 2, s[:offset]
    return -1, ""


def evaluate2(inputs: numpy.ndarray):
    outs = []
    for index in range(inputs.size):
        string = ""
        ins: numpy.ndarray = numpy.copy(inputs)
        while ins.size > 0:
            if index >= ins.size:
                index = 0
            i: numpy.uint8 = ins[index]
            if string == "":
                string += '{:02X}'.format(i)
                ins = numpy.delete(ins, index)
                continue
            found = False
            for j, o in enumerate(ins):
                other = '{:02X}'.format(o)
                t, label = similar(other, string, 1)
                if t == 1:
                    string += label
                    ins = numpy.delete(ins, j)
                    found = True
                    break
                elif t == 2:
                    string = label + string
                    ins = numpy.delete(ins, j)
                    found = True
                    break

            # print(string)
            if not found:
                for j, o in enumerate(ins):
                    other = '{:02X}'.format(o)
                    t, label = similar(other, string, 1)
                    if t == 1:
                        string += label
                        ins = numpy.delete(ins, j)
                        found = True
                        break
                    elif t == 2:
                        string = label + string
                        ins = numpy.delete(ins, j)
                        found = True
                        break
            # print(string)
            if not found:
                string += '{:02X}'.format(i)
                ins = numpy.delete(ins, index)
            # print(string)
            index += 1
        outs.append(string)
    return sorted(outs, key=len)[0]


def hex_to_bytes(s: str) -> bytearray:
    a = bytearray()
    #   256 128 64  32  16  8   4   2   1
    #   0   0   1   0   0   1   0   0   1
    #   1   0   0   0   0   1   1   0   1
    #   0   0   1   0   0   0   0   1   1
    #       0   1   1   0   0   1   1   0
    s += "0" * (len(s) % 2)
    index = 0
    while index < len(s):
        part = s[index:index+2]
        index += 2
        # print(part, int(part, 16))
        a.append(int(part, 16))
    return a


def main(folder: str, input: str):
    bar = Bar("Reading file", max=5)
    bar.start()
    with open(f"{folder}/{input}", "rb") as f:
        line = f.read()
        n = 2
        s: numpy.ndarray = numpy.frombuffer(line, dtype=numpy.uint8)
        # s = [memoryview(line, i, i+n) for i in range(0, len(line), n)]

    bar.message = "Evaluating"
    bar.next()

    # o = test(s, lambda b, a: stat(b, a, 4))
    unique = numpy.unique(s)
    o = evaluate2(unique)
    bar.message = "Hex to bytes"
    bar.next()
    b = hex_to_bytes(o)
    bar.message = "Writing"
    bar.next()

    # writing encrypted file
    with open(f"{folder}/encrypted.bytes", "wb") as f:
        f.write(b)

    a = Array('uint8', b).data

    bar.message = "Creating indexes - map"
    bar.next()

    _map = {}

    for item in unique:
        _bin = bin(item).removeprefix("0b")
        _bin = "0b" + "0"*(8 - len(_bin)) + _bin
        tup = a.findall(_bin, bytealigned=False)
        indices = [x for x in tup if (x % 4) == 0]
        _map[item] = numpy.uint8(indices[0] / 4)

    bar.message = "Creating indexes"
    bar.next()

    lam = numpy.zeros(len(s), dtype=numpy.uint8)

    for index, val in enumerate(s):
        lam[index] = _map[val]

    """def get_index(val: numpy.uint8):
        _bin = bin(val).removeprefix("0b")
        _bin = "0b" + "0"*(8 - len(_bin)) + _bin
        tup = a.findall(_bin, bytealigned=False)
        indices = [x for x in tup if (x % 4) == 0]
        return numpy.uint8(indices[0] / 4)

    lam = numpy.vectorize(get_index)(s)"""

    bar.finish()
    print()

    return lam

    # return [o.index('{:02X}'.format(c)) for c in s]


if __name__ == "__main__":
    exit(1)
