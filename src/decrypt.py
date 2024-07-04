from bitstring import BitArray, Bits
from bits import str_to_bits
from huffman_algorithm import read_frequencies, decrypt, evaluate


def read_bits(hexes, size):
    last = ""
    bb = []
    for c in hexes:
        val = int(c, 16)
        b = bin(val).removeprefix("0b")
        b = "0" * (4 - len(b)) + b
        last += b
        if len(last) >= size:
            bits = last[0:size]
            bb.append(str_to_bits(bits))
            last = last[size:]
    return bb


def read(bits: BitArray):
    header, shortcuts, indexes = bits.split(delimiter=f'0x{"0f"*8}', count=3)
    shortcuts: BitArray = shortcuts[64:]
    indexes: BitArray = indexes[64:]
    i_size = header[0:4].uint
    s_size = header[4:8].uint

    shorts = list(shortcuts.cut(s_size))
    indices = list(indexes.cut(i_size))

    return shorts, indices


def load(shorts, indexes):
    values = []
    for index in indexes:
        values.append(shorts[index.uint].uint)
    return values


def read_huffman(bits: BitArray):
    header, shortcuts, indexes = bits.split(delimiter=f'0x{"0f"*8}', count=3)
    shortcuts: BitArray = shortcuts[64:]
    indexes: BitArray = indexes[64:]
    added = header.uint
    
    remaining = shortcuts.len % 9
    shortcuts = shortcuts[0:-remaining]

    table: list[Bits] = list(shortcuts.cut(9))
    freqs = read_frequencies(table)
    freqs = dict(sorted(freqs.items()))
    codes = evaluate(freqs)

    decryption = decrypt(indexes[0:-added] if added != 0 else indexes, codes)
    return decryption


def main(folder: str, is_huffman: bool):
    barray = bytearray()
    with open(f"{folder}/encrypted.bytes", "rb") as f:
        b = f.read()
        hexes = b.hex()

    # print(hexes)

    if is_huffman:
        with open(f"{folder}/word.pass", "rb") as f:
            cnt = f.read()
            bits = BitArray(cnt)

            indexes = read_huffman(bits)
            for i in indexes:
                if i == "":
                    continue
                index = int(i)
                h = hexes[index:index+2]
                barray.append(int(h, 16))

        with open(f"{folder}/decrypted", "wb") as f:
            f.write(barray)
    else:
        with open(f"{folder}/word.pass", "rb") as f:
            a, b = read(BitArray(f.read()))
            indexes = load(a, b)
            for i in indexes:
                if i == "":
                    continue
                h = hexes[i:i+2]
                barray.append(int(h, 16))

        with open(f"{folder}/decrypted", "wb") as f:
            f.write(barray)


if __name__ == "__main__":
    exit(1)
