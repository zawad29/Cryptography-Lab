import math
import numpy as np
import re
from encrypt import vigenere_decipher

REGEX = '[^A-Za-z]'

frequency = {'E': 12.0,
             'T': 9.10,
             'A': 8.12,
             'O': 7.68,
             'I': 7.31,
             'N': 6.95,
             'S': 6.28,
             'R': 6.02,
             'H': 5.92,
             'D': 4.32,
             'L': 3.98,
             'U': 2.88,
             'C': 2.71,
             'M': 2.61,
             'F': 2.30,
             'Y': 2.11,
             'W': 2.09,
             'G': 2.03,
             'P': 1.82,
             'B': 1.49,
             'V': 1.11,
             'K': 0.69,
             'X': 0.17,
             'Q': 0.11,
             'J': 0.10,
             'Z': 0.07}


def predictKeyLen(text):
    text = text.lower()
    counts = []
    for i in range(1, int(len(text)/2)):
        cnt = 0
        for j in range(len(text)-i):
            if(text[i+j] == text[j]):
                cnt += 1
        counts.append(cnt)
    # print(counts)
    avg = np.average(counts)
    sdv = np.std(counts)
    predicted_pos = []
    prev_index = -1
    for i in range(1, len(counts)):
        if counts[i-1] > avg+1.5*sdv:
            if(prev_index == -1):
                prev_index = i
            else:
                predicted_pos.append(i-prev_index)
    return predicted_pos[0]


def predictKey(text, keylen):
    text = text.upper()
    buckets = ['']*keylen
    for i in range(len(text)):
        buckets[i % keylen] += text[i]
    # print(buckets)
    key = ''
    for bucket in buckets:
        freq = {}
        for c in bucket:
            freq[c] = 1 if c not in freq else freq[c] + 1
        for c in freq.keys():
            freq[c] = freq[c]*100/len(bucket)
        min_error = 100
        ch = '#'
        for j in range(0, 26):
            error = 0.0
            for i in range(0, 26):
                shifted_pos = 65+(i+j) % 26
                if chr(shifted_pos) in freq:
                    error += abs(frequency[chr(65+i)] - freq[chr(shifted_pos)])
            if error < min_error:
                min_error = error
                ch = chr(j+65)
        key = key + ch
    return key


def ioc(text):
    text = text.lower()
    freq = [0]*26
    N = 0
    for i in text:
        if(i >= 'a' and i <= 'z'):
            N += 1
            freq[ord(i)-97] += 1
    # print(freq)
    total = 0
    for i in range(0, 26):
        total += freq[i] * (freq[i] - 1)
    total = 26*total/N/(N-1)
    # print(total)
    return total


def vigenere_hack():
    with open("input.txt", "r+") as inputfile, open("key.txt", "r") as keyfile, open("output.txt", "r+") as outputfile, open("deciphered.txt", "w") as originalfile:
        # input = inputfile.read()
        input = outputfile.read()
        input = re.sub(REGEX, '',  input)
        keylen = predictKeyLen(input)
        key = predictKey(input, keylen)
        print(f'Predicted key length: {keylen}')
        print(f'Predicted key : {key}')
        original = vigenere_decipher(input, key)
        originalfile.write(original)


if __name__ == "__main__":
    vigenere_hack()
