import heapq
import numpy
from collections import Counter
from progress.bar import Bar
from optimize_pass import get_delimiter
from bitstring import Bits, BitArray


class Node:
    def __init__(self, character, frequency, left=None, right=None):
        self.character = character
        self.frequency = frequency
        self.left = left
        self.right = right

    def __lt__(self, other):
        if not isinstance(other, Node):
            exit(1)
        return self.frequency < other.frequency

    def __repr__(self):
        return f"Node({self.character}, {self.frequency})"


def get_frequencies(s: bytearray):
    frequencies = {}
    for c in s:
        if c not in frequencies:
            frequencies[c] = 0
        frequencies[c] += 1
    return frequencies


def get_codes(tree_list: list[Node]):
    code = {}

    def get_code(tree: Node, b):
        if tree is None:
            return
        get_code(tree.left, b + Bits([0]))
        if tree.character is not None:
            code[tree.character] = b
        get_code(tree.right, b + Bits([1]))

    get_code(tree_list[0], Bits(0))
    return code


def create_sub(sub: numpy.ndarray, codes: dict[int, str]):
    return "".join([codes[c] for c in sub])


def gen_string(s: numpy.ndarray, codes: dict[int, Bits]) -> BitArray:
    a = BitArray()

    # for i in range(n):
    #    jobs.append(pool.apply_async(create_sub, (partitions[i], codes, )))
    for c in s:
        a += codes[c]

    return a  # "".join([job.get() for job in jobs])


def search_value(d: dict[int, Bits], val: Bits):
    for key, value in d.items():
        if value == val:
            # print(key, val, value == val)
            return key
    return None


def decrypt(s: Bits, codes: dict[int, Bits]) -> bytearray:
    final = bytearray()
    last = Bits(0)
    for bit in s:
        _bit = Bits([bit])
        new = last + _bit

        key = search_value(codes, new)
        if key is None:
            last += _bit
        else:
            final.append(key)
            last = Bits(0)
    return final


def evaluate(freqs: dict):
    tlist = []
    for ch, freq in freqs.items():
        tlist.append(Node(ch, freq))
    heapq.heapify(tlist)
    while len(tlist) != 1:
        t1: Node = heapq.heappop(tlist)
        t2: Node = heapq.heappop(tlist)
        t3 = Node(None, t1.frequency + t2.frequency, t1, t2)
        heapq.heappush(tlist, t3)

    return get_codes(tlist)


"""
0F0F 0F0F 0F0F 0F0F => delimiter
TREE
8 bits -> char
1 bit -> relative frequency
SHORTCUTS
$shortcut size$ bits -> one index
INDEXES
$index size$ bits -> shortcut reference
"""


def write_frequencies(freqs: dict[numpy.uint8, Bits]):
    s = sorted(freqs.items(), key=lambda x: x[1])
    table = Bits(0)
    last = None
    for item in s:
        relative = 0
        if last is not None:
            relative = item[1] - last[1]
        c: numpy.uint8 = item[0]

        b = Bits()
        for i in range(8):
            b += Bits([(c & (1 << (7 - i))) != 0])
        b += Bits([relative])

        table += b

        last = item
    return table


def read_frequencies(bits: list[Bits]):
    index = 1
    freqs = {}
    for b in bits:
        rel = int(b[-1])
        c = b[0:8].uint
        index += rel
        freqs[c] = index
    return scale_dict(freqs)


def scale_dict(original_dict: dict):
    m = max(min(original_dict.values()) - 1, 0)
    for k in original_dict.keys():
        original_dict[k] -= m
    # Extract the frequencies
    # Extract unique frequencies and sort them
    unique_frequencies = sorted(set(original_dict.values()))

    # Create a mapping from original frequencies to new smaller values
    frequency_mapping = {freq: i + 1 for i, freq in enumerate(unique_frequencies)}

    # Create the new dictionary with the mapped frequencies
    scaled_dict = {key: frequency_mapping[value] for key, value in original_dict.items()}

    return scaled_dict


def create_pass(folder: str, indexes: numpy.ndarray):
    bar = Bar("Getting and scaling frequencies", max=5)
    bar.start()

    freqs = scale_dict(Counter(indexes))
    bar.message = "Sorting frequencies"
    bar.next()
    freqs = dict(sorted(freqs.items()))

    bar.message = "Evaluating"
    bar.next()
    # t = write_frequencies(freqs)
    # freqs = read_frequencies(read_table(t))
    codes = evaluate(freqs)

    bar.message = "Generating string"
    bar.next()

    out = gen_string(indexes, codes)

    i = 0
    while ((out.len + i) % 8) != 0:
        i += 1
    added = i

    bar.message = "Writing frequencies"
    bar.next()

    t = write_frequencies(freqs)

    table = t.tobytes()
    data = out.tobytes()

    header = bytearray([added])

    bar.message = "Writing into file"
    bar.next()

    with open(f"{folder}/word.pass", "wb") as f:
        final_data = header + get_delimiter() + table + get_delimiter() + data

        a = 0
        while (len(final_data) % 8) != 0:
            final_data.append(0x00)
            a += 8
        header[0] += a

        final_data[0] = header[0]
        f.write(final_data)
    bar.finish()
    print()
    return len(table), len(data)


if __name__ == '__main__':
    exit(1)
