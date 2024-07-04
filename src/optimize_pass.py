from bits import *

"""
0F0F 0F0F 0F0F 0F0F => delimiter
HEADERS
4 bits -> shortcut sizes
4 bits -> indices sizes
SHORTCUTS
$shortcut size$ bits -> one index
INDEXES
$index size$ bits -> shortcut reference
"""


def bits_for_max(max_num: int) -> int:
    return len(bin(max_num).removeprefix("0b"))


def get_delimiter() -> bytearray:
    return bytearray([0x0F for _ in range(8)])


def write(folder, infos):
    barray = bytearray()
    i_size = infos["indexes"]["size"]
    s_size = infos["shortcuts"]["size"]
    barray.append((i_size << 4) + s_size)
    # delimiter
    barray += get_delimiter()

    b = []
    for shortcut in infos["shortcuts"]["buffer"]:
        bs = bin(shortcut).removeprefix("0b")
        bs = "0" * (s_size - len(bs)) + bs
        b.append(str_to_bits(bs))

    final = unite(b)
    index = 0
    while index < len(final):
        part = final[index:index + 8]
        index += 8
        barray.append(int(part, 2))

    # delimiter
    barray += get_delimiter()

    b = []
    for i in infos["indexes"]["buffer"]:
        bs = bin(i).removeprefix("0b")
        bs = "0" * (i_size - len(bs)) + bs
        b.append(str_to_bits(bs))

    final = unite(b)
    index = 0
    while index < len(final):
        part = final[index:index + 8]
        index += 8
        barray.append(int(part, 2))

    with open(f"{folder}/word.pass", "wb") as f:
        f.write(barray)


def create_pass(folder: str, indexes: list):
    no_duplicates = list(set(indexes))
    max_index = max(indexes)
    nd = len(no_duplicates)-1

    indices = []
    for i in indexes:
        indices.append(no_duplicates.index(i))

    for_indexes = bits_for_max(nd)
    for_shortcuts = bits_for_max(max_index)

    write(folder, {
        "indexes": {
            "buffer": indices,
            "size": for_indexes
        },
        "shortcuts": {
            "buffer": no_duplicates,
            "size": for_shortcuts
        }
    })
    return for_indexes, for_shortcuts


def main(folder: str):
    with open(f"{folder}/word.pass") as f:
        indexes = [int(i) for i in f.read().split(" ")[:-1]]
    create_pass("", indexes)


if __name__ == "__main__":
    exit(1)
