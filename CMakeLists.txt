cmake_minimum_required(VERSION 3.24)
project(Test C)

set(CMAKE_C_STANDARD 23)

add_library(
        Main
        C_Code/Map/map.c
        C_Code/Map/map.h
        C_Code/Utils/utils.h
        C_Code/Utils/utils.c
        C_Code/BitArray/bitarray.h
        C_Code/BitArray/bitarrray.c
        C_Code/Huffman/huffman_algorithm.h
        C_Code/Huffman/huffman_algorithm.c
        C_Code/Huffman/huffman.c
)

add_executable(Analyze
        analyze.c
        C_Code/Encrypt/encrypt.c
        C_Code/Encrypt/encrypt.h
        C_Code/Decrypt/decrypt.h
        C_Code/Decrypt/decrypt.c
)
target_link_libraries(Analyze Main)
