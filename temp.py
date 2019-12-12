from sha1 import sha_1


def check_sign_dsa(**kwargs):
    """
    The function checks the electronic digital signature (DSA, SHA-1).
    :param kwargs: p,q,y...;
    :return: True or error message with explanation;
    """

    try:
        p = int(kwargs.get('p', 0))
        q = int(kwargs.get('q', 0))
        y = int(kwargs.get('y', 0))
        h = int(kwargs.get('h', 0))
    except:
        return 'Convert error.'

    filename = kwargs.get('filename')

    if filename is not None:
        r = 13
        s = 79
        byte_array = bytearray()

        hash_obj = sha_1(byte_array)
        my_hash = int(hash_obj.hexdigest(), 16)

        g = fastEXP(h, ((p - 1) // q), p)
        w = fastEXP(s, q - 2, q)

        u1 = (my_hash * w) % q
        u2 = (r * w) % q

        v = ((fastEXP(g, u1, p) * fastEXP(y, u2, p)) % p) % q

        if r == v:
            return True
        else:
            return False

    return 'File error'


if __name__ == '__main__':
    check = check_sign_dsa(p=809, q=101, y=204, filename='input.txt')
    print(check)
