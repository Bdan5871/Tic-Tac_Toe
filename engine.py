import monte_carlo_tree_search
import numpy as np
import shared
import time


class Engine(object):

    def __init__(self, policy_net, value_net):
        self.policy_net = policy_net
        self.value_net = value_net

    def generate_sets(self, games, simulations):
        policy_network_training_set = []
        value_network_training_set = []
        start = time.time()
        seconds = -10
        for i in range(games):
            end = time.time()
            if end - start >= seconds + 10:
                print("Played " + str(i) + " games.")
                seconds = end - start
            node = monte_carlo_tree_search.MonteCarloTreeNode([['.', '.', '.'], ['.', '.', '.'], ['.', '.', '.']])
            zed = node.get_zed()
            turns = 0
            while zed is None:
                a_t, pi_t = self.get_optimal_move(node.s, simulations, True)
                x = shared.s_to_x(node.s)
                policy_network_training_set.append([x, pi_t])
                value_network_training_set.append([x, None])
                node = node.make_move(a_t)
                turns += 1
                zed = node.get_zed()
            for k in range(1, turns + 1):
                zed *= -1
                value_network_training_set[-k][1] = np.reshape([zed], (1, 1))
        print("Played " + str(games) + " games.")
        return policy_network_training_set, value_network_training_set

    def get_optimal_move(self, s_root, simulations, exploration=False):
        pi_t = monte_carlo_tree_search.search(s_root, self.policy_net, self.value_net, simulations)
        if exploration:
            return np.random.choice([a for a in range(9)], p=np.reshape(pi_t, 9)), pi_t
        else:
            return np.argmax(np.reshape(pi_t, 9)), pi_t
