import math
import matplotlib.pyplot as plt
from scipy.integrate import dblquad
from random import random


def multiplicatively_congruent(alpha, beta, n):
    m = 2147483648
    brv = [(beta * alpha) % m]
    for i in range(1, n):
        brv.append((beta * brv[i - 1]) % m)
        brv[i - 1] /= m
    brv[n - 1] /= m
    return brv


def modeling_r(n, alpha=704219, beta=704219):
    brv = multiplicatively_congruent(alpha, beta, n)
    r_arr = []
    for i in range(n):
        r_arr.append(math.sqrt(6 * brv[i] + 1))
    return r_arr


def modeling_phi(n):
    phi_arr = []
    i = 0
    while i < n:
        random_value = random()
        value = 2 * math.pi * random_value - 0.499
        check = (2 * value - math.sin(2 * value)) / (4 * math.pi)
        if random_value < check:
            phi_arr.append(value)
            i += 1
    return phi_arr


def integral(n):
    r_arr = modeling_r(n)
    phi_arr = modeling_phi(n)
    res = 0
    for i in range(n):
        res += function(phi_arr[i], r_arr[i]) * 3 * math.pi / (r_arr[i] * math.sin(phi_arr[i]) ** 2)
    return res / n


def expected_value(vec):
    res = 0
    for item in vec:
        res += item
    return res / len(vec)


def dispersion(vec):
    avg = expected_value(vec)
    res = 0
    for item in vec:
        res += pow(item - avg, 2)
    return res / (len(vec) - 1)


def function(phi, r):
    return ((r * math.cos(phi)) ** 3 + math.exp(r * math.sin(phi))) / (r * (1 + math.sin(phi) ** 2))


def check_integral(func):
    return dblquad(func, 1, math.sqrt(7), lambda r: 0, lambda r: 2 * math.pi)[0]


def main():
    n = 10000
    value = integral(n)
    exact_value = check_integral(function)
    print("Monte-Carlo: {}".format(value))
    print("Exact value: {}".format(exact_value))

    arr = []
    for i in range(5, 501):
        arr.append(integral(i))
    plt.plot(list(range(5, 501)), [exact_value] * 496, color='red')
    plt.plot(list(range(5, 501)), arr)
    plt.show()


if __name__ == "__main__":
    main()