import numpy as np

c_base = 1
c_init = 0


def s_to_x(s):
    policy_x = np.zeros((2, 3, 3))
    value_x = np.full((2, 3, 3), -1)
    for i in range(3):
        for j in range(3):
            if s[i][j] == 'X':
                policy_x[0][i][j] = 1
                value_x[0][i][j] = 1
            elif s[i][j] == 'O':
                policy_x[1][i][j] = 1
                value_x[1][i][j] = 1
    return np.reshape(policy_x, (18, 1)), np.reshape(value_x, (18, 1))
