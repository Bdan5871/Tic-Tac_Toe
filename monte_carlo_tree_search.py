import shared
import copy
import numpy as np


class MonteCarloTreeNode(object):

    def __init__(self, s):
        self.s = s
        self.N = 0
        self.W = 0
        self.Q = 0
        self.P = 0
        self.children = []

    def C(self):
        return np.log((1 + self.N + shared.c_base) / shared.c_base) + shared.c_init

    def expand(self, p, v):
        denominator = 0
        for a in range(9):
            self.children.append(self.make_move(a))
            if self.children[a] is not None:
                self.children[a].P = np.exp(p[a][0])
                denominator += self.children[a].P

        for a in range(9):
            if self.children[a] is not None:
                self.children[a].P /= denominator

    def get_a_t(self):
        a_t = -1
        maximum_PUCT = -np.inf
        for a in range(9):
            if self.children[a] is not None:
                PUCT = self.children[a].Q + self.U(a)
                if PUCT > maximum_PUCT:
                    a_t = a
                    maximum_PUCT = PUCT
        return a_t

    def get_player(self):
        turns = 0
        for i in range(3):
            for j in range(3):
                if self.s[i][j] != '.':
                    turns += 1
        if turns % 2:
            return 'O'
        else:
            return 'X'

    def get_zed(self):
        if self.is_win():
            return 1
        if self.is_draw():
            return 0
        return None

    def is_draw(self):
        # assumes node is not win
        for i in range(3):
            for j in range(3):
                if self.s[i][j] == '.':
                    return False
        return True

    def is_leaf(self):
        # assumes node is not terminal node
        return len(self.children) == 0

    def is_win(self):
        # check for row win
        for i in range(3):
            if self.s[i][0] != '.':
                win = True
                for j in range(1, 3):
                    if self.s[i][j] != self.s[i][0]:
                        win = False
                        break
                if win:
                    return True

        # check for column win
        for j in range(3):
            if self.s[0][j] != '.':
                win = True
                for i in range(1, 3):
                    if self.s[i][j] != self.s[0][j]:
                        win = False
                        break
                if win:
                    return True

        # check for main-diagonal win
        if self.s[0][0] != '.':
            win = True
            for i in range(1, 3):
                if self.s[i][i] != self.s[0][0]:
                    win = False
                    break
            if win:
                return True

        # check for anti-diagonal win
        if self.s[0][2] != '.':
            win = True
            for i in range(1, 3):
                if self.s[i][2 - i] != self.s[0][2]:
                    win = False
                    break
            if win:
                return True

        return False

    def make_move(self, a):
        if self.s[a // 3][a % 3] != '.':
            return None
        s = copy.deepcopy(self.s)
        s[a // 3][a % 3] = self.get_player()
        return MonteCarloTreeNode(s)

    def U(self, a):
        return self.C() * self.children[a].P * np.sqrt(self.N) / (1 + self.children[a].N)


def simulate(node, policy_net, value_net):
    zed = node.get_zed()
    if zed is not None:
        node.N += 1
        node.W += zed
        node.Q = node.W / node.N
        return zed

    if node.is_leaf():
        policy_x, value_x = shared.s_to_x(node.s)
        p, v = policy_net.feedforward(policy_x), np.argmax(value_net.feedforward(value_x))
        node.expand(p, v)
        node.N += 1
        node.W += v
        node.Q = node.W / node.N
        return v

    a_t = node.get_a_t()
    v = -simulate(node.children[a_t], policy_net, value_net)
    node.N += 1
    node.W += v
    node.Q = node.W / node.N
    return v


def search(simulations, s_0, policy_net, value_net):
    node = MonteCarloTreeNode(s_0)
    for i in range(simulations):
        simulate(node, policy_net, value_net)
    pi = []
    for a in range(9):
        if node.children[a] is not None:
            pi.append(node.children[a].N)
        else:
            pi.append(0)
    return np.reshape(pi, (9, 1)) / sum(pi)
