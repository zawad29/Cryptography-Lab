from BitVector import *
PASSPHRASE = "Hopes and dreams of a million years"
BLOCKSIZE = 16
HINT = "Douglas Adams"


def decrypt(text, key):
    numbytes = BLOCKSIZE // 8
    # Reduce the passphrase to a bit array of size BLOCKSIZE:
    bv_iv = BitVector(bitlist=[0]*BLOCKSIZE)  # (F)
    for i in range(0, len(PASSPHRASE) // numbytes):  # (G)
        textstr = PASSPHRASE[i*numbytes:(i+1)*numbytes]  # (H)
        bv_iv ^= BitVector(textstring=textstr)  # (I)
    # Create a bitvector from the ciphertext hex string:
    encrypted_bv = BitVector(hexstring=text)  # (K)
    # Reduce the key to a bit array of size BLOCKSIZE:
    key_bv = BitVector(intVal=key, size=BLOCKSIZE)
    # Create a bitvector for storing the decrypted plaintext bit array:
    msg_decrypted_bv = BitVector(size=0)  # (T)
    # Carry out differential XORing of bit blocks and decryption:
    previous_decrypted_block = bv_iv  # (U)
    for i in range(0, len(encrypted_bv) // BLOCKSIZE):  # (V)
        bv = encrypted_bv[i*BLOCKSIZE:(i+1)*BLOCKSIZE]  # (W)
        temp = bv.deep_copy()  # (X)
        bv ^= previous_decrypted_block  # (Y)
        previous_decrypted_block = temp
        bv ^= key_bv  # (a)
        msg_decrypted_bv += bv  # (b)
    # Extract plaintext from the decrypted bitvector:
    outputtext = msg_decrypted_bv.get_text_from_bitvector()  # (c)
    return outputtext


def brute_force_attack(ciphered_text):
    # loop through keys and test
    for key in range(29500, 2**BLOCKSIZE - 1):
        outputtext = decrypt(ciphered_text, key)
        # check if outputtext contain the hint
        if outputtext.find(HINT) != -1:
            return outputtext, key


if __name__ == '__main__':
    with open("ciphered_text.txt", 'r') as inputfile, open("deciphered_text.txt", 'w') as outputfile, open("key.txt", 'w') as keyfile:
        ciphered_text = inputfile.read()
        deciphered_text, key = brute_force_attack(ciphered_text)
        keyfile.write(str(key))
        outputfile.write(deciphered_text[:-1])
        print(key)
        print(deciphered_text)
