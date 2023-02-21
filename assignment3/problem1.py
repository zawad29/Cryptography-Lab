
# Given cipher texts
C1 = [0xe9, 0x3a, 0xe9, 0xc5, 0xfc, 0x73, 0x55, 0xd5]
C2 = [0xf4, 0x3a, 0xfe, 0xc7, 0xe1, 0x68, 0x4a, 0xdf]

length = len(C1)
# C1 xor C2
M = []
for i in range(length):
    M.append(C1[i] ^ C2[i])

# decrypt
with open('dict.txt', 'r') as dictionary:
    words = dictionary.read().split()
    words = set([word for word in words if len(word) == length])
    for word1 in words:
        M1 = [ord(c) for c in word1]
        M2 = []
        for i in range(length):
            M2.append(M1[i] ^ M[i])
        word2 = ''.join([chr(c) for c in M2])
        if word2 in words:
            print(word1, word2)

print('done')
