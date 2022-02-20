import monte_carlo_tree_search
import numpy as np

import policy_network
import shared
import value_network


class Engine(object):

    def __init__(self, policy_net, value_net):
        self.policy_net = policy_net
        self.value_net = value_net

    def generate_sets(self, games, simulations):
        policy_network_training_set = []
        value_network_training_set = []

        for i in range(games):
            node = monte_carlo_tree_search.MonteCarloTreeNode([['.', '.', '.'], ['.', '.', '.'], ['.', '.', '.']])
            zed = node.get_zed()
            turns = 0

            while zed is None:
                a_t, pi_t = self.get_move(simulations, node.s, self.policy_net, self.value_net, True)
                policy_x, value_x = shared.s_to_x(node.s)
                policy_network_training_set.append([policy_x, pi_t])
                value_network_training_set.append([value_x, None])
                node = node.make_move(a_t)
                turns += 1
                zed = node.get_zed()

            for k in range(1, turns + 1):
                value_network_training_set[-k][1] = np.reshape([zed], (1, 1))
                zed *= -1

        return policy_network_training_set, value_network_training_set

    def get_move(self, simulations, s_root, policy_net, value_net, exploration=False):
        pi_t = monte_carlo_tree_search.search(simulations, s_root, policy_net, value_net)

        if exploration:
            return np.random.choice([a for a in range(9)], p=np.reshape(pi_t, 9)), pi_t
        else:
            return np.argmax(np.reshape(pi_t, 9)), pi_t

    def get_optimal_move(self, simulations, s_root):
        pi_t = monte_carlo_tree_search.search(simulations, s_root, self.policy_net, self.value_net)
        return np.argmax(np.reshape(pi_t, 9)), pi_t

    def train(self, steps, training_games, training_simulations, policy_net_sizes, value_net_sizes,
              policy_net_epochs, policy_net_mini_batch_size, policy_net_eta, policy_net_c,
              value_net_epochs, value_net_mini_batch_size, value_net_eta, value_net_c,
              test_games, test_simulations, policy_net_file, value_net_file):
        for i in range(steps):
            policy_net_training_set, value_net_training_set = self.generate_sets(training_games, training_simulations)
            print("Training sets generated.")

            policy_net = policy_network.PolicyNetwork(policy_net_sizes)
            value_net = value_network.ValueNetwork(value_net_sizes)

            policy_net.stochastic_gradient_descent(policy_net_training_set, policy_net_epochs, policy_net_mini_batch_size, policy_net_eta, policy_net_c)
            print("Policy network training complete.")

            value_net.stochastic_gradient_descent(value_net_training_set, value_net_epochs, value_net_mini_batch_size, value_net_eta, value_net_c)
            print("Value network training complete.")

            wins = self.test(policy_net, value_net, test_games, test_simulations)
            if wins >= test_games - wins:
                print("New engine " + str(wins / (test_games - wins)) + " times stronger than current engine.")

                policy_net.save(policy_net_file)
                policy_net.save(value_net_file)

                self.policy_net = policy_net
                self.value_net = value_net

            print("Step " + str(i + 1) + " complete.")
            print()

    def test(self, policy_net, value_net, games, simulations):
        wins = 0

        for i in range(games):
            node = monte_carlo_tree_search.MonteCarloTreeNode([['.', '.', '.'], ['.', '.', '.'], ['.', '.', '.']])
            zed = node.get_zed()
            turns = 0

            while zed is None:
                if (i + turns) % 2:
                    a_t, pi_t = self.get_move(simulations, node.s, policy_net, value_net)
                else:
                    a_t, pi_t = self.get_move(simulations, node.s, self.policy_net, self.value_net)

                node = node.make_move(a_t)
                turns += 1
                zed = node.get_zed()

            if (i % 2 + turns % 2) % 2:
                zed *= -1

            wins += (zed + 1) / 2

        return wins
