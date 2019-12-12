from sha1 import sha_1
import shutil


def fast_multiplying(a, digree, number):
    x = 1
    while digree != 0:
        while digree % 2 == 0:
            digree //= 2
            a = (a**2) % number
        digree -= 1
        x = (x * a) % number
    return x


def DSA(filename, q, p, h, x, k):
    g = get_g(h, p, q)
    if g < 2:
        raise ValueError
    y = fast_multiplying(g, x, p)
    with open(filename, 'rb') as f:
        text = f.read()
    hash = sha_1(text)
    r = (fast_multiplying(g, k, p)) % q
    s = (fast_multiplying(k, q - 2, q) * ((hash + x * r)) % q)
    if r == 0 or s == 0:
        raise ValueError
    pos = filename.rfind('.')
    ds_filename = filename[:pos] + '(ds)' + filename[pos:]
    shutil.copy(filename, ds_filename)
    with open(ds_filename, 'a') as f:
        f.write('\n' + str(r))
        f.write('\n' + str(s))
    return hash, r, s


def check_digital_signature(filename, q, p, h, x, k):
    with open(filename, 'r') as f:
        text = f.read().split('\n')
    try:
        s = int(text[-1])
        r = int(text[-2])
        text.pop(-1)
        text.pop(-1)
        text = '\n'.join(text).encode()
    except:
        return False, None, None
    g = get_g(h, p, q)
    hash = sha_1(text)
    y = fast_multiplying(g, x, p)
    w = fast_multiplying(s, q - 2, q)
    u1 = (hash * w) % q
    u2 = (r * w) % q
    v = (fast_multiplying(g, u1, p) * fast_multiplying(y, u2, p) % p) % q
    if v == r:
        return True, v, r
    return False, v, r


def get_g(h, p, q):
    return fast_multiplying(h, (p - 1) // q, p)
