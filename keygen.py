import hashlib
from constants import *

def rot_word(x: int):
    return ((x >> 24) | (x << 8)) & MASK

def sub_word(x: int):
    return (SBOX[x >> 28][x >> 24 & 0xf] << 24) | (SBOX[x >> 20 & 0xf][x >> 16 & 0xf] << 16) | (SBOX[x >> 12 & 0xf][x >> 8 & 0xf] << 8) | SBOX[x >> 4 & 0xf][x & 0xf]

def to_bytes(x: int):
    return x.to_bytes(4, 'big')

def to_key(x0, x1, x2, x3):
    return to_bytes(x0) + to_bytes(x1) + to_bytes(x2) + to_bytes(x3)

def key_expansion(x: bytes):
    int_x = int(hashlib.md5(x).hexdigest(), 16)

    x0 = (int_x >> 96) & MASK
    x1 = (int_x >> 64) & MASK
    x2 = (int_x >> 32) & MASK
    x3 = int_x & MASK

    keys = []

    for i in range(ROUND):
        x0 = sub_word(rot_word(x0)) ^ RCON[i]
        x1 ^= x0
        x2 ^= x1
        x3 ^= x2
        keys.append(to_key(x0, x1, x2, x3))
    
    return keys

if __name__ == "__main__":
    key = b"test"
    keys = key_expansion(key)
    for i in range(ROUND):
        print(keys[i])