from keygen import key_expansion
from constants import *
from Sbox import SBox
from PBox import PBox
from binascii import hexlify, unhexlify

def pad(input: bytes) -> bytes:
    pad_len = BLOCK_SIZE - (len(input) % BLOCK_SIZE)
    pad = chr(pad_len).encode('latin-1') * pad_len
    return input + pad

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
        # subtitusi dengan sbox
        substituted_1 = sbox.subBytes(list(cipherblock), False)
        # permutasi dengan pbox
        permutted = pbox.permute_all(substituted_1, False)
        # subtitusi dengan rijndael
        substituted_2 = subs(permutted)
        # xor dengan key
        cipherblock = int.from_bytes(substituted_2, 'big') ^ int.from_bytes(keys[i], 'big')
        cipherblock = cipherblock.to_bytes(BLOCK_SIZE, 'big')
    return cipherblock

def encrypt(plaintext: bytes, key: bytes):
    sbox = SBox(key)
    pbox = PBox([7,2,0,15,12,10,14,8,6,11,1,9,13,4,5,3])
    keys = key_expansion(key)
    plaintext = pad(plaintext)
    ciphertext = b""

    for i in range(0, len(plaintext), BLOCK_SIZE):
        ciphertext += encrypt_block(plaintext[i:i+BLOCK_SIZE], keys, sbox, pbox)

    return ciphertext

def decrypt_block(block: bytes, keys: list, sbox: SBox, pbox: PBox):
    plainblock = block
    for i in range(ROUND-1, -1, -1):
        # xor dengan key
        plainblock = int.from_bytes(plainblock, 'big') ^ int.from_bytes(keys[i], 'big')
        plainblock = plainblock.to_bytes(BLOCK_SIZE, 'big')
        # subtitusi dengan rijndael
        substituted_2 = inv_subs(plainblock)
        # permutasi dengan pbox
        permutted = pbox.permute_all(substituted_2, True)
        # subtitusi dengan sbox
        substituted_1 = sbox.subBytes(permutted, True)
        plainblock = bytes(substituted_1)
    return plainblock

def decrypt(ciphertext: bytes, key: bytes):
    sbox = SBox(key)
    pbox = PBox([7,2,0,15,12,10,14,8,6,11,1,9,13,4,5,3])
    keys = key_expansion(key)
    plaintext = b""

    for i in range(0, len(ciphertext), BLOCK_SIZE):
        plaintext += decrypt_block(ciphertext[i:i+BLOCK_SIZE], keys, sbox, pbox)

    return plaintext

if __name__ == "__main__":
    key = b"test"
    plaintext = b"halo-halo bandung"
    arrPlainText = [byte for byte in plaintext]
    print("plaintext:", arrPlainText)
    ciphertext = encrypt(plaintext, key)
    arrCipherText = [byte for byte in ciphertext]
    print("ciphertext:", arrCipherText)
    decryptRes = decrypt(ciphertext, key)
    arrDecryptRes = [byte for byte in decryptRes]
    print("plaintext:", arrDecryptRes)