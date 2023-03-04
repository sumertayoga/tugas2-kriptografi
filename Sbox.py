import hashlib
from binascii import unhexlify

def binToHexa(n):
    # convert binary to int
    num = int(n, 2)

    # convert int to hexadecimal
    hex_num = format(num, 'x')
    paddingLength = 32 - len(hex_num)
    for i in range(paddingLength):
        hex_num = "0" + hex_num
    return(hex_num)


def cyclicShift(binaryString):
    # Melakukan pergeseran 1 bit ke kiri secara siklik
    temp = binaryString[4:]
    return temp + binaryString[:4]


def xorBinary(binary1, binary2):
    # Melakukan xor dua binarystring
    # dan outputkan binarystring hasilnya
    # dengan padding agar panjang bit tetap 128
    temp = bin(int(binary1, 2) ^ int(binary2, 2))[2:]
    paddingLength = 128 - len(temp)
    for i in range(paddingLength):
        temp = "0" + temp
    return temp


class SBox():
    def __init__(self, key):
        key = hashlib.md5(key.encode('utf-8'))
        res = bin(int(key.hexdigest(), 16)).zfill(8)[2:]

        tempArr = [res]
        for i in range(15):
            tempArr.append(xorBinary(tempArr[i], cyclicShift(tempArr[i])))
        for i in range(16):
            tempArr[i] = binToHexa(tempArr[i])

        tempMat = [[0 for _ in range(16)] for _ in range(16)]
        for i in range(16):
            for j in range(16):
                tempMat[i][j] = int(tempArr[i][j*2:j*2+2], 16)
        self.sbox_table = tempMat

    def substitute(self, input):
        row = (input & 0x0f)
        col = input >> 4
        return self.sbox_table[row][col]

    def subBytes(self, bytess):
        ciphertext = b''
        for byte in bytess:
            ciphertext += self.substitute(byte).to_bytes(1, 'big')
        return ciphertext

