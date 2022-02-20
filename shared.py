import numpy as np

c_base = 19652
c_init = 2.5


def s_to_x(s):
    xs = []
    os = []
    for i in range(3):
        xs.append([])
        os.append([])
        for j in range(3):
            xs[i].append(0)
            os[i].append(0)
            if s[i][j] == 'X':
                xs[i][j] = 1
            elif s[i][j] == 'O':
                os[i][j] = 1
    return np.reshape([xs, os], (18, 1))
