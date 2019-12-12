class Var:
    A = 0x67452301
    B = 0xEFCDAB89
    C = 0x98BADCFE
    D = 0x10325476
    E = 0xC3D2E1F0


def get_key(t):
    if t < 20:
        return 0x5A827999
    if t < 40:
        return 0x6ED9EBA1
    if t < 60:
        return 0x8F1BBCDC
    if t < 80:
        return 0xCA62C1D6


def get_func_res(x, y, z, t):
    if t < 20:
        return (x & y) | (~x & z)
    if t < 40:
        return x ^ y ^ z
    if t < 60:
        return (x & y) | (x & z) | (y & z)
    if t < 80:
        return x ^ y ^ z


def get_int(b_array):
    return (b_array[0] << 24) + (b_array[1] << 16) + (b_array[2] << 8) + b_array[3]


def get_W(text):
    W = []
    for t in range(16):
        W.append(get_int(text[t * 4: (t + 1) * 4]))
    for t in range(16, 80):
        W.append(rol(W[t - 3] ^ W[t - 8] ^ W[t - 14] ^ W[t - 16], 1))
    return W


def bytes_from_file(filename, chunksize=64):
    with open(filename, "rb") as f:
        while True:
            chunk = f.read(chunksize)
            if chunk:
                for b in chunk:
                    yield b
            else:
                break


def rol(number, shift):
    return ((number << shift) | (number >> (32 - shift))) & 0xffffffff


def sha_1(text):
    blocks_of_text = [bytearray()]
    counter = 0
    len_of_text = 0
    for b in text:
        counter += 1
        len_of_text += 8
        blocks_of_text[-1].append(b)
        if counter == 64:
            counter = 0
            blocks_of_text.append(bytearray())
    last_block = len(blocks_of_text[-1]) + 1
    blocks_of_text[-1].append(128)
    if last_block > 56:
        for i in range(last_block, 64):
            blocks_of_text[-1].append(0)
        blocks_of_text.append(bytearray())
        for i in range(56):
            blocks_of_text[-1].append(0)
    else:
        for i in range(last_block, 56):
            blocks_of_text[-1].append(0)
    temp = (len_of_text).to_bytes(8, byteorder='big')
    for i in range(8):
        blocks_of_text[-1].append(temp[i])
    main_var = Var()
    for text in blocks_of_text:
        var = Var()
        W = get_W(text)
        for t in range(80):
            temp = (rol(var.A, 5) + get_func_res(var.B, var.C, var.D,
                                                 t) + var.E + get_key(t) + W[t]) & 0xffffffff
            var.E = var.D
            var.D = var.C
            var.C = rol(var.B, 30)
            var.B = var.A
            var.A = temp
        main_var.A = (main_var.A + var.A) & 0xffffffff
        main_var.B = (main_var.B + var.B) & 0xffffffff
        main_var.C = (main_var.C + var.C) & 0xffffffff
        main_var.D = (main_var.D + var.D) & 0xffffffff
        main_var.E = (main_var.E + var.E) & 0xffffffff
    return (main_var.A << 128) + (main_var.B << 96) + (main_var.C << 64) + (main_var.D << 32) + main_var.E


if __name__ == '__main__':
    print(hex(sha_1("input.txt")))
