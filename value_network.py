import json
import numpy as np


class ValueNetwork(object):

    def __init__(self, sizes):
        self.L = len(sizes)
        self.sizes = sizes
        self.w = [np.random.randn(y, x) for x, y in zip(sizes[:-1], sizes[1:])]
        self.b = [np.random.randn(x, 1) for x in sizes[1:]]

    def backpropagation(self, s, zed):
        a_l = s
        a = [a_l]
        z = []

        for w_l, b_l in zip(self.w, self.b):
            z_l = w_l @ a_l + b_l
            z.append(z_l)
            a_l = tanh(z_l)
            a.append(a_l)

        delta_w = [np.zeros(w_l.shape) for w_l in self.w]
        delta_b = [np.zeros(b_l.shape) for b_l in self.b]

        delta_l = c_prime(a[-1], zed) * tanh_prime(z[-1])
        delta_w[-1] = delta_l @ a[-2].transpose()
        delta_b[-1] = delta_l

        for k in range(2, self.L):
            delta_l = self.w[-k + 1].transpose() @ delta_l * tanh_prime(z[-k])
            delta_w[-k] = delta_l @ a[-k - 1].transpose()
            delta_b[-k] = delta_l

        return delta_w, delta_b

    def feedforward(self, s):
        a_l = s
        for w_l, b_l in zip(self.w, self.b):
            a_l = tanh(w_l @ a_l + b_l)
        return a_l

    def get_average_cost(self, test_set):
        total_cost = 0
        for s, zed in test_set:
            total_cost += mean_squared_error(self.feedforward(s), zed)
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
                print("Accuracy on test set: " + str(self.accuracy(test_set)))
                print("Average cost on test set: " + str(self.get_average_cost(test_set)))

    def save(self, network_file):
        with open(network_file, 'w') as f:
            json.dump({'sizes': self.sizes,
                       'w': [w_l.tolist() for w_l in self.w],
                       'b': [b_l.tolist() for b_l in self.b]}, f)

    def update(self, mini_batch, eta, c):
        total_delta_w = [np.zeros(w_l.shape) for w_l in self.w]
        total_delta_b = [np.zeros(b_l.shape) for b_l in self.b]

        for s, zed in mini_batch:
            delta_w, delta_b = self.backpropagation(s, zed)
            total_delta_w = [total_delta_w_l + delta_w_l for total_delta_w_l, delta_w_l in zip(total_delta_w, delta_w)]
            total_delta_b = [total_delta_b_l + delta_b_l for total_delta_b_l, delta_b_l in zip(total_delta_b, delta_b)]

        self.w = [(1 - eta * 2 * c / len(mini_batch)) * w_l - eta * total_delta_w_l / len(mini_batch) for w_l, total_delta_w_l in zip(self.w, total_delta_w)]
        self.b = [b_l - eta * total_delta_b_l / len(mini_batch) for b_l, total_delta_b_l in zip(self.b, total_delta_b)]


def c_prime(v, zed):
    return 2 * (v - zed)


def load(file):
    f = open(file)
    parameters = json.load(f)
    f.close()

    network = ValueNetwork(parameters['sizes'])
    network.w = [np.asarray(w_l) for w_l in parameters['w']]
    network.b = [np.asarray(b_l) for b_l in parameters['b']]

    return network


def mean_squared_error(v, zed):
    return np.linalg.norm(zed - v) ** 2


def sigmoid(z):
    return 1 / (1 + np.exp(-z))


def tanh(z):
    return 2 * sigmoid(2 * z) - 1


def tanh_prime(z):
    return 1 - tanh(z) ** 2

