class State():
    def __init__(self, state):
        self.state = state
    
    def shift_rows(self):
        for i in range(0, 4):
            self.state[i] = self.state[i][i:] + self.state[i][:i]
        return self.state

if __name__ == '__main__':
    state = State([
        [0x63, 0xca, 0xb7, 0x04],
        [0x09, 0x53, 0xd0, 0x51],
        [0xcd, 0x60, 0xe0, 0xe7],
        [0xba, 0x70, 0x1f, 0x9f]
    ])
    ciphertext = state.shift_rows()
    print(ciphertext)
