#include <stdio.h>
#include <stdlib.h>
#include "Encrypt/encrypt.h"
#include "Decrypt/decrypt.h"
#include "Huffman/huffman_algorithm.h"

size_t get_file_size(const char* filename) {
    FILE* file = fopen(filename, "r");
    if (file == NULL)
        exit(1);
    fseek(file, 0L, SEEK_END);
    size_t size = ftell(file);
    fclose(file);
    return size;
}

int main() {
    int status;
    //printf("%llu\n", get_file_size("../tests/C/encrypted.bytes"));

    FILE* file_ptr = fopen("../tests/txt/input.txt", "rb");  // Open the file in binary mode
    if (file_ptr == NULL)
        return 1;

    size_t res_len;
    int* indexes = NULL;
    status = encrypt(file_ptr, &indexes, &res_len);
    if (status != 0 || indexes == NULL)
        return status;

    status = create_huffman_pass(indexes, res_len);

    if (status != 0)
        return status;

    status = decrypt();
    if (status != 0)
        return status;

    return 0;
}