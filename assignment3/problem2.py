import json


def encode(m, p, prev_c):
    return (m ^ (p + prev_c) % 256)


def encrypt(word, P, prev_c=0):  # word = String, P = Int List
    W = [ord(c) for c in word]
    C = []
    for i in range(len(P)):
        Ci = encode(W[i], P[i], prev_c)
        C.append(Ci)
        prev_c = Ci
    return C


def decrypt(C, P, prev_c=0):  # C = Int List, P = Int List
    W = []
    for i in range(len(P)):
        Wi = encode(C[i], P[i], prev_c)
        prev_c = C[i]
        W.append(Wi)
    word = ''.join([chr(c) for c in W])
    return word


def task1():
    PAD = [12, 15, 1, 123, 55, 33, 90, 190, 72, 29]
    c = encrypt('MangoJuice', PAD)
    print('cipher: ', c)
    word = decrypt(c, PAD)
    print('message: ', word)


ciphertexts = []    # given ciphertexts
# messages = []       # message to find
msg_count = 10      # number of ciphertexts
msg_len = 60        # length of each text
pads = []           # possible pads
words = []          # dictionary words
w_interval = 15     # word interval for pad search


# hack the cipher and find message and pad
def hack(index, last_index, pad):
    global words, ciphertexts, pads, msg_count, msg_len
    message = ''    # initialize the message
    if index == last_index:
        start_index = last_index - w_interval
        for ciphertext in ciphertexts:
            msg = str(decrypt(ciphertext[start_index:last_index], pad,
                      prev_c=ciphertext[start_index-1] if start_index > 0 else 0))
            message += (msg.lower() + '\n')
        score = sum(len(word)**2 for word in words if word in message)
        return (pad, message, score)
    # Else
    best_score = 0
    best_message = None
    best_pad = None
    for p in pads[index]:
        curr_pad, curr_message, curr_score = hack(
            index=index+1, last_index=last_index, pad=pad + [p])    # recuesive hack
        # log message and score
        # with open('msglog.txt', 'a') as msglog:
        #     msglog.write(str(curr_score) + '\n')
        #     msglog.write(curr_message + '\n')
        if curr_score > best_score:    # find the best combination and return
            best_score = curr_score
            best_message = curr_message
            best_pad = curr_pad
    return (best_pad, best_message, best_score)

# the given task2 to hack the cipher from the 10 ciphertexts encrypted using same pad


def task2():
    global words, ciphertexts, pads, msg_count, msg_len
    # list of valid charcters
    valid_chars = list(range(65, 91)) + list(range(97, 123)
                                             ) + [32, 44, 46, 63, 33, 45, 40, 41]
    # get the dictionary words
    with open('dict.txt', 'r') as dictionary:
        words = dictionary.read().lower().split()
    # get the 10 cipher texts from given file
    with open('ciphertext.txt', 'r') as ciphertextfile:
        for i in range(10):
            ciphertexts.append(json.loads(ciphertextfile.readline()))

    # find the possible pads for each position
    # this is done using the valid chars
    # test all possible pad bytes, if it decrypts all the string to valid chars, it may be a possible pad
    for j in range(msg_len):
        possible_pad = []
        for i in range(256):
            valid = 1
            for k in range(msg_count):
                prev_c = ciphertexts[k][j-1] if j > 0 else 0
                m = encode(ciphertexts[k][j], i, prev_c)
                if not (valid_chars.__contains__(m)):
                    valid = 0
                    break
            if valid == 1:
                possible_pad.append(i)
        pads.append(possible_pad)
    pad_lens = list(len(p) for p in pads)
    print('possible pad counts: ', pad_lens)

    # clear the message log
    # with open('msglog.txt', 'w') as msglog:
    #     msglog.write('')

    # empty list to contain the deciphered messages
    messages = []
    for i in range(msg_count):
        messages.append('')
    pad = []

    # divide the ciphertexts into intervals and hack seperately because hacking the whole texts at once has huge complexity
    # this helps reduce complexity
    # find messages and pads seperately and stitch them together
    i = 0       # starting index
    while i < msg_len:
        l = i
        r = i + w_interval
        i = r
        if(r >= msg_len):
            r = msg_len
        new_pad, new_message, score = hack(index=l, last_index=r, pad=[])
        print(new_pad)
        print(new_message)
        pad += new_pad
        new_messages = new_message.split('\n')
        for j in range(msg_count):
            messages[j] += new_messages[j]

    # join the messages into a single string
    message = '\n'.join(messages)

    # save the result to a file
    with open('hacked_message.txt', 'w') as msgfile, open('hacked_pad.txt', 'w') as padfile:
        msgfile.write(str(message))
        padfile.write(str(pad))


if __name__ == "__main__":
    task2()
