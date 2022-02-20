import json
import numpy as np


class PolicyNetwork(object):

    def __init__(self, sizes):
        self.L = len(sizes)
        self.sizes = sizes
        self.w = [np.random.randn(y, x) for x, y in zip(sizes[:-1], sizes[1:])]
        self.b = [np.random.randn(x, 1) for x in sizes[1:]]

    def backpropagation(self, s, pi):
        a_l = s
        a = [a_l]
        z = []

        for l in range(self.L - 2):
            z_l = self.w[l] @ a_l + self.b[l]
            z.append(z_l)
            a_l = sigmoid(z_l)
            a.append(a_l)

        z_l = self.w[-1] @ a_l + self.b[-1]
        z.append(z_l)
        a_l = softmax(z_l)
        a.append(a_l)

        delta_w = [np.zeros(w_l.shape) for w_l in self.w]
        delta_b = [np.zeros(b_l.shape) for b_l in self.b]

        delta_l = a[-1] - pi
        delta_w[-1] = delta_l @ a[-2].transpose()
        delta_b[-1] = delta_l

        for k in range(2, self.L):
            delta_l = self.w[-k + 1].transpose() @ delta_l * sigmoid_prime(z[-k])
            delta_w[-k] = delta_l @ a[-k - 1].transpose()
            delta_b[-k] = delta_l

        return delta_w, delta_b

    def feedforward(self, s):
        a_l = s
        for l in range(self.L - 2):
            a_l = sigmoid(self.w[l] @ a_l + self.b[l])
        return softmax(self.w[-1] @ a_l + self.b[-1])

    def get_average_cost(self, test_set):
        total_cost = 0
        for s, pi in test_set:
            total_cost += cross_entropy_losses(self.feedforward(s), pi)
        return total_cost / len(test_set)

    def stochastic_gradient_descent(self, training_set, epochs, mini_batch_size, eta, c, test_set):
        N = len(training_set)
        for i in range(epochs):
            np.random.shuffle(training_set)
            mini_batches = [training_set[j: j + mini_batch_size] for j in range(0, N, mini_batch_size)]
            for mini_batch in mini_batches:
                self.update(mini_batch, eta, c)
            print("Epoch " + str(i + 1) + " complete.")
            if test_set:
                print("Average cost on test set: " + str(self.get_average_cost(test_set)))

    def save(self, file):
        with open(file, 'w') as f:
            json.dump({'sizes': self.sizes,
                       'w': [w_l.tolist() for w_l in self.w],
                       'b': [b_l.tolist() for b_l in self.b]}, f)

    def update(self, mini_batch, eta, c):
        total_delta_w = [np.zeros(w_l.shape) for w_l in self.w]
        total_delta_b = [np.zeros(b_l.shape) for b_l in self.b]

        for s, pi in mini_batch:
            delta_w, delta_b = self.backpropagation(s, pi)
            total_delta_w = [total_delta_w_l + delta_w_l for total_delta_w_l, delta_w_l in zip(total_delta_w, delta_w)]
            total_delta_b = [total_delta_b_l + delta_b_l for total_delta_b_l, delta_b_l in zip(total_delta_b, delta_b)]

        self.w = [(1 - eta * 2 * c / len(mini_batch)) * w_l - eta * total_delta_w_l / len(mini_batch) for w_l, total_delta_w_l in zip(self.w, total_delta_w)]
        self.b = [b_l - eta * total_delta_b_l / len(mini_batch) for b_l, total_delta_b_l in zip(self.b, total_delta_b)]


def cross_entropy_losses(p, pi):
    return np.sum(-pi * np.log(p))


def load(file):
    f = open(file)
    parameters = json.load(f)
    f.close()

    network = PolicyNetwork(parameters['sizes'])
    network.w = [np.asarray(w_l) for w_l in parameters['w']]
    network.b = [np.asarray(b_l) for b_l in parameters['b']]

    return network


def sigmoid(z):
    return 1 / (1 + np.exp(-z))


def sigmoid_prime(z):
    return sigmoid(z) * (1 - sigmoid(z))


def softmax(z):
    return np.exp(z - max(z)) / sum(np.exp(z - max(z)))
