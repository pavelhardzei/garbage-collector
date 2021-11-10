import math
import matplotlib.pyplot as plt


def multiplicatively_congruent(alpha, beta, n):
    m = 2147483648
    brv = [(beta * alpha) % m]
    for i in range(1, n):
        brv.append((beta * brv[i - 1]) % m)
        brv[i - 1] /= m
    brv[n - 1] /= m
    return brv


def modeling_exponential_distribution(lam, n, alpha=704219, beta=704219):
    brv = multiplicatively_congruent(alpha, beta, n)
    exponential_distribution = list()
    for i in range(n):
        exponential_distribution.append(-math.log(brv[i]) / lam)
    return exponential_distribution


def first_integral(n):
    exponential_distribution = modeling_exponential_distribution(1, n)
    res = 0
    for rv in exponential_distribution:
        res += math.exp(rv - rv ** 4) * math.sqrt(1 + rv ** 2)
    res = 2 * res / n
    return res


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


def get_final_rv(n):
    distribution = modeling_exponential_distribution(1, n)
    for i in range(n):
        rv = distribution[i]
        distribution[i] = math.exp(rv - rv ** 4) * math.sqrt(1 + rv ** 2)
    return distribution


def print_to_file(n):
    with open("file.txt", "w", encoding="utf-8") as file:
        rv1 = modeling_exponential_distribution(1, n)
        rv2 = get_final_rv(n)
        for i in range(n):
            print("{}\t\t\t-\t{}".format(rv1[i], rv2[i]), file=file)


def main():
    n = 100
    value = first_integral(n)
    exact_value = 2.07959
    print("Monte-Carlo: {}".format(value))
    print("Exact value: {}".format(exact_value))
    print("Probabilistic error: {:.2f}".format(0.6745 * math.sqrt(dispersion(get_final_rv(n))) / n))

    errors = list()
    for i in range(5, 101):
        errors.append(0.6745 * math.sqrt(dispersion(get_final_rv(i))) / i)
    plt.plot(list(range(5, 101)), errors)
    plt.show()


if __name__ == "__main__":
    main()