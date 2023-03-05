from keygen import key_expansion
from constants import *
from Sbox import SBox
from PBox import PBox


def pad(input: bytes) -> bytes:
    if(len(input) % BLOCK_SIZE != 0):
        pad_len = BLOCK_SIZE - (len(input) % BLOCK_SIZE)
        pad = chr(pad_len).encode('latin-1') * pad_len
        input += pad
    return input


def unpad(input: bytes) -> bytes:
    pad_len = input[-1]
    return input[:-pad_len]


def subs(bytess):
    substituted = []
    for byte in bytess:
        substituted.append(SBOX[byte >> 4][byte & 0xf])
    return substituted


def inv_subs(bytess):
    substituted = []
    for byte in bytess:
        substituted.append(INV_SBOX[byte >> 4][byte & 0xf])
    return substituted


def encrypt_block(block: bytes, keys: list, sbox: SBox, pbox: PBox):
    cipherblock = block
    for i in range(ROUND):
        left = cipherblock[0:8]
        right = cipherblock[8:]
        # subtitusi dengan sbox
        substituted_1 = sbox.subBytes(list(right), False)
        # permutasi dengan pbox
        permutted = pbox.permute_all(substituted_1, False)
        # subtitusi dengan rijndael
        substituted_2 = subs(permutted)
        # xor dengan key
        cipherblock = int.from_bytes(
            substituted_2, 'big') ^ int.from_bytes(keys[i][0:8], 'big')
        
        cipherblock = cipherblock ^ int.from_bytes(left, 'big')
        cipherblock = cipherblock.to_bytes(8, 'big')
        cipherblock = right + cipherblock
    return cipherblock


def encrypt(plaintext: bytes, key: bytes):
    sbox = SBox(key)
    pbox = PBox([6, 3, 0, 4, 2, 7, 5, 1])
    keys = key_expansion(key)
    plaintext = pad(plaintext)
    ciphertext = b""

    for i in range(0, len(plaintext), BLOCK_SIZE):
        ciphertext += encrypt_block(plaintext[i:i +
                                    BLOCK_SIZE], keys, sbox, pbox)

    return ciphertext


def decrypt_block(block: bytes, keys: list, sbox: SBox, pbox: PBox):
    plainblock = block
    for i in range(ROUND-1, -1, -1):
        left = plainblock[0:8]
        right = plainblock[8:]
        # subtitusi dengan sbox
        substituted_1 = sbox.subBytes(list(left), False)
        # permutasi dengan pbox
        permutted = pbox.permute_all(substituted_1, False)
        # subtitusi dengan rijndael
        substituted_2 = subs(permutted)
        # xor dengan key
        plainblock = int.from_bytes(
            substituted_2, 'big') ^ int.from_bytes(keys[i][0:8], 'big')
        plainblock = plainblock ^ int.from_bytes(right, 'big')
        plainblock = plainblock.to_bytes(8, 'big')
        plainblock = plainblock + left
    return plainblock


def decrypt(ciphertext: bytes, key: bytes):
    sbox = SBox(key)
    pbox = PBox([6, 3, 0, 4, 2, 7, 5, 1])
    keys = key_expansion(key)
    plaintext = b""

    for i in range(0, len(ciphertext), BLOCK_SIZE):
        plaintext += decrypt_block(ciphertext[i:i +
                                   BLOCK_SIZE], keys, sbox, pbox)

    return plaintext


if __name__ == "__main__":
    key = b"test"
    plaintext = b"halo-halobandunt"
    print("plaintext:", list(plaintext))
    ciphertext = encrypt(plaintext, key)
    print("ciphertext:", list(ciphertext))
    decryptRes = decrypt(ciphertext, key)
    # decryptRes = unpad(decryptRes)
    print("plaintext:", list(decryptRes))
    plaintext2 = b"halo-halobandung"
    print("plaintext2:", list(plaintext2))
    ciphertext2 = encrypt(plaintext2, key)
    print("ciphertext2:", list(ciphertext2))
    decryptRes2 = decrypt(ciphertext2, key)
    # decryptRes = unpad(decryptRes)
    print("plaintext2:", list(decryptRes2))
