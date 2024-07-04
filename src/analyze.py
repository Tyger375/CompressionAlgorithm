import os.path

from encrypt import main as encrypt
from decrypt import main as decrypt
from optimize_pass import create_pass
from huffman_algorithm import create_pass as create_huffman_pass
import time


def debug(stats: dict, other_stats: dict, start_time):
    header = "{:<15}| {:<15}| {:<15}| {:<15}".format("File", "Bytes", "Bits", "KB")
    print(header)
    print("-" * len(header))
    for k, v in stats.items():
        print(f"{k:<15}| {f'{v:,}':<15}| {f'{v * 8:,}':<15}| {f'{v / 1000:.2f}':<15}")

    for k, v in other_stats.items():
        print(f"{k:<15}| {v:<15}| {' ':<15}| {' ':<15}")

    print(f"- Executed in {(time.time() - start_time):.2f} seconds")


def with_shortcuts(folder, file):
    start_time = time.time()
    indexes = encrypt(folder, file)
    a, b = create_pass(folder, indexes)
    decrypt(folder, False)

    input_size = os.path.getsize(f"{folder}/{file}")
    encrypted_size = os.path.getsize(f"{folder}/encrypted.bytes")
    indexes_size = os.path.getsize(f"{folder}/word.pass")
    total_size = encrypted_size + indexes_size

    stats = {
        "input": input_size,
        "encrypted": encrypted_size,
        "indexes": indexes_size,
        "total": total_size,
        "efficiency": input_size - total_size
    }
    debug(stats, {
        "size shortcuts": f"{b} bits",
        "size indexes": f"{a} bits"
    }, start_time)


def with_huffman(folder, file):
    start_time = time.time()
    indexes = encrypt(folder, file)
    a, b = create_huffman_pass(folder, indexes)
    decrypt(folder, True)

    input_size = os.path.getsize(f"{folder}/{file}")
    encrypted_size = os.path.getsize(f"{folder}/encrypted.bytes")
    indexes_size = os.path.getsize(f"{folder}/word.pass")
    total_size = encrypted_size + indexes_size

    stats = {
        "input": input_size,
        "encrypted": encrypted_size,
        "indexes": indexes_size,
        "total": total_size,
        "efficiency": input_size - total_size
    }
    debug(stats, {
        "size indexes": f"{b} bytes",
        "size table": f"{a} bytes"
    }, start_time)


def simple_debug(folder: str, file: str):
    input_size = os.path.getsize(f"{folder}/{file}")
    encrypted_size = os.path.getsize(f"{folder}/encrypted.bytes")
    indexes_size = os.path.getsize(f"{folder}/word.pass")
    total_size = encrypted_size + indexes_size

    stats = {
        "input": input_size,
        "encrypted": encrypted_size,
        "indexes": indexes_size,
        "total": total_size,
        "efficiency": input_size - total_size
    }

    debug(stats, {}, time.time())


if __name__ == "__main__":
    f1 = "tests/txt"
    f2 = "input.txt"

    # f1 = "tests/txt"
    # f2 = "input.txt"
    print("WITH SHORTCUTS".center(66, "-"))
    with_shortcuts(f1, f2)
    print("")
    print("WITH HUFFMAN".center(66, "-"))
    with_huffman(f1, f2)
