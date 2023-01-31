'''
encryption part
'''


def encode(i, k):
    kval = (ord(k) - 97) if k >= 'a' and k <= 'z' else (ord(k)-65)
    if i >= 'a' and i <= 'z':
        return chr((ord(i) + kval - 97) % 26 + 97)
    else:
        return chr((ord(i) + kval - 65) % 26 + 65)


def vigenere_cipher(input, key):
    output = ""
    keylen = len(key)
    kindex = 0
    for i in input:
        if not ((i >= 'a' and i <= 'z') or (i >= 'A' and i <= 'Z')):
            continue
        if(kindex > 0 and kindex % 5 == 0):
            output = output + " "
        o = encode(i, key[kindex % keylen])
        output = output + o
        kindex += 1
    return output


def encrypt():
    with open("input.txt", "r") as inputfile, open("key.txt", "r") as keyfile, open("output.txt", "w") as outputfile:
        input = inputfile.read()
        key = keyfile.read()
        output = vigenere_cipher(input, key)
        # print(output)
        outputfile.write(output)


'''
decrypt to original text
'''


def decode(i, k):
    kval = (ord(k) - 97) if k >= 'a' and k <= 'z' else (ord(k)-65)
    kval = 26 - kval
    if i >= 'a' and i <= 'z':
        return chr((ord(i) + kval - 97) % 26 + 97)
    else:
        return chr((ord(i) + kval - 65) % 26 + 65)


def vigenere_decipher(input, key):
    output = ""
    keylen = len(key)
    kindex = 0
    for i in input:
        if not ((i >= 'a' and i <= 'z') or (i >= 'A' and i <= 'Z')):
            continue
        o = decode(i, key[kindex % keylen])
        output = output + o
        kindex += 1
    return output


def decrypt():
    with open("original.txt", "w") as originalfile, open("key.txt", "r") as keyfile, open("output.txt", "r") as outputfile:
        input = outputfile.read()
        key = keyfile.read()
        original = vigenere_decipher(input, key)
        # print(original)
        originalfile.write(original)


if __name__ == "__main__":
    encrypt()
    decrypt()
