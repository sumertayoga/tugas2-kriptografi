class PBox():
    def __init__(self, pbox_table):
        self.pbox_table = pbox_table
    
    def permute(self, input):
        array =[]
        for i in range(len(input)):
            array.append(input[self.pbox_table[i]])
        return array


if __name__ == '__main__':
    p16 = PBox([7,2,0,15,12,10,14,8,6,11,1,9,13,4,5,3])
    p = [0x63, 0x7C, 0x77, 0x7B, 0xF2, 0x6B, 0x6F, 0xC5, 0x30, 0x01, 0x67, 0x2B, 0xFE, 0xD7, 0xAB, 0x76]
    plaintext = b'\x63\x7c\x77\x7b\xf2\x6b\x6f\xc5\x30\x01\x67\x2b\xfe\xd7\xab\x76'
    ciphertext = p16.permute( plaintext)
    



