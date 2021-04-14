import math
import scipy.stats


def multiplicatively_congruent(alpha, beta, n):
    m = 2147483648
    brv = [(beta * alpha) % m]
    for i in range(1, n):
        brv.append((beta * brv[i - 1]) % m)
        brv[i - 1] /= m
    brv[n - 1] /= m
    return brv


def modeling_normal_distribution(m, s_2, n, alpha=704219, beta=704219):
    brv = multiplicatively_congruent(alpha, beta, 12 * n)
    normal_distribution_rv = list()
    for i in range(n):
        normal_distribution_rv.append(-6)
        for j in range(12):
            normal_distribution_rv[i] += brv[12 * i + j]
        normal_distribution_rv[i] = m + math.sqrt(s_2) * normal_distribution_rv[i]
    return normal_distribution_rv


def modeling_laplace_distribution(a, n, alpha=704219, beta=704219):
    brv = multiplicatively_congruent(alpha, beta, n)
    laplace_distribution_rv = list()
    for i in range(n):
        if brv[i] < 0.5:
            laplace_distribution_rv.append(math.log(2 * brv[i]) / a)
        else:
            laplace_distribution_rv.append(-math.log(2 * (1 - brv[i])) / a)
    return laplace_distribution_rv


def modeling_weibull_distribution(a, b, n, alpha=704219, beta=704219):
    brv = multiplicatively_congruent(alpha, beta, n)
    weibull_distribution_rv = list()
    for i in range(n):
        weibull_distribution_rv.append(pow(-math.log(brv[i]) / a, 1 / b))
    return weibull_distribution_rv


def modeling_cauchy_distribution(a, b, n, alpha=696617, beta=696617):
    brv = multiplicatively_congruent(alpha, beta, n)
    cauchy_distribution_rv = list()
    for i in range(n):
        cauchy_distribution_rv.append(a + b * math.tan(math.pi * (brv[i] - 0.5)))
    return cauchy_distribution_rv


def modeling_logistic_distribution(a, b, n, alpha=704219, beta=704219):
    brv = multiplicatively_congruent(alpha, beta, n)
    logistic_distribution_rv = list()
    for i in range(n):
        logistic_distribution_rv.append(a + b * math.log(brv[i] / (1 - brv[i])))
    return logistic_distribution_rv


def empirical_func(x, vec):
    res = 0
    for item in vec:
        if item < x:
            res += 1
    return res / len(vec)


def laplace_distribution(x):
    a = 0.5
    if x < 0:
        return pow(math.e, a * x) / 2
    return 1 - pow(math.e, -a * x) / 2


def weibull_distribution(x):
    a = 1
    b = 0.5
    return 1 - pow(math.e, -a * x ** b)


def cauchy_distribution(x):
    a = -1
    b = 1
    return 1 / 2 + math.atan((x - a) / b) / math.pi


def logistic_distribution(x):
    a = 2
    b = 3
    return pow(1 + pow(math.e, (a - x) / b), -1)


def kolmogorov(vec, distribution):
    partition = 25
    lower_bound = min(vec)
    step = (max(vec) - lower_bound) / partition
    dn = 0
    for i in range(1, partition + 1):
        point = lower_bound + i * step
        temp = math.fabs(empirical_func(point, vec) - distribution(point))
        if dn < temp:
            dn = temp
    return math.sqrt(len(vec)) * dn < 1.36


def pearson(vec, distribution):
    partition = 25
    lower_bound = min(vec)
    if lower_bound >= 0:
        lower_bound = 0
    step = (max(vec) - lower_bound) / partition
    frequency = [0] * partition
    for item in vec:
        index = int((item - lower_bound) / step)
        if index == partition:
            index -= 1
        frequency[index] += 1
    res = 0
    for i in range(1, partition + 1):
        delta = len(vec) * (distribution(lower_bound + i * step) - distribution(lower_bound + (i - 1) * step))
        res += pow((frequency[i - 1] - delta), 2) / delta
    return res < 37.7


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


def main():
    primes = list()
    with open("primes.txt", "r") as file:
        primes = list(map(int, file.read().split()))

    n = 1000
    m = 0
    s_2 = 1
    normal_distribution_rv = modeling_normal_distribution(m, s_2, n)
    with open("../bin/normal_distribution_rc.txt", "w", encoding='utf-8') as file:
        for rv in normal_distribution_rv:
            print(rv, file=file)
    print('Нормальное распределение:\n\tМатематическое ожидание: {}\t-\t{}'
          .format(expected_value(normal_distribution_rv), m))
    print('\tДисперсия: {}\t-\t{}'.format(dispersion(normal_distribution_rv), s_2))
    print('\tКритерий Колмогорова: {}'.format(kolmogorov(normal_distribution_rv, scipy.stats.norm(m, s_2).cdf)))
    print('\tКритерий Пирсона: {}'.format(pearson(normal_distribution_rv, scipy.stats.norm(m, s_2).cdf)))
    res_kolmogorov = 0
    res_pearson = 0
    for i in range(100):
        if not kolmogorov(modeling_normal_distribution(m, s_2, n, primes[i], primes[i]), scipy.stats.norm(m, s_2).cdf):
            res_kolmogorov += 1
        if not pearson(modeling_normal_distribution(m, s_2, n, primes[i], primes[i]), scipy.stats.norm(m, s_2).cdf):
            res_pearson += 1
    print('\tВероятность ошибки первого рода(Колмогоров): {}%'.format(res_kolmogorov))
    print('\tВероятность ошибки первого рода(Пирсон): {}%\n'.format(res_pearson))

    a = 0.5
    laplace_distribution_rv = modeling_laplace_distribution(a, n)
    with open("../bin/laplace_distribution_rc.txt", "w", encoding='utf-8') as file:
        for rv in laplace_distribution_rv:
            print(rv, file=file)
    print('Распределение Лапласа:\n\tМатематическое ожидание: {}\t-\t{}'
          .format(expected_value(laplace_distribution_rv), 0))
    print('\tДисперсия: {}\t-\t{}'.format(dispersion(laplace_distribution_rv), 2 / a ** 2))
    print('\tКритерий Колмогорова: {}'.format(kolmogorov(laplace_distribution_rv, laplace_distribution)))
    print('\tКритерий Пирсона: {}'.format(pearson(laplace_distribution_rv, laplace_distribution)))
    res_kolmogorov = 0
    res_pearson = 0
    for i in range(100):
        if not kolmogorov(modeling_laplace_distribution(a, n, primes[i], primes[i]), laplace_distribution):
            res_kolmogorov += 1
        if not pearson(modeling_laplace_distribution(a, n, primes[i], primes[i]), laplace_distribution):
            res_pearson += 1
    print('\tВероятность ошибки первого рода(Колмогоров): {}%'.format(res_kolmogorov))
    print('\tВероятность ошибки первого рода(Пирсон): {}%\n'.format(res_pearson))

    a = 1
    b = 0.5
    weibull_distribution_rv = modeling_weibull_distribution(a, b, n)
    with open("../bin/weibull_distribution_rc.txt", "w", encoding='utf-8') as file:
        for rv in weibull_distribution_rv:
            print(rv, file=file)
    print('Распределение Вейбулла:\n\tМатематическое ожидание: {}\t-\t{}'
          .format(expected_value(weibull_distribution_rv), pow(a, -1 / b) * math.gamma(1 + 1 / b)))
    print('\tДисперсия: {}\t-\t{}'.format(dispersion(weibull_distribution_rv),
                                          pow(a, -2 / b) * (math.gamma(1 + 2 / b) - math.gamma(1 + 1 / b) ** 2)))
    print('\tКритерий Колмогорова: {}'.format(kolmogorov(weibull_distribution_rv, weibull_distribution)))
    print('\tКритерий Пирсона: {}'.format(pearson(weibull_distribution_rv, weibull_distribution)))
    res_kolmogorov = 0
    res_pearson = 0
    for i in range(100):
        if not kolmogorov(modeling_weibull_distribution(a, b, n, primes[i], primes[i]), weibull_distribution):
            res_kolmogorov += 1
        if not pearson(modeling_weibull_distribution(a, b, n, primes[i], primes[i]), weibull_distribution):
            res_pearson += 1
    print('\tВероятность ошибки первого рода(Колмогоров): {}%'.format(res_kolmogorov))
    print('\tВероятность ошибки первого рода(Пирсон): {}%\n'.format(res_pearson))

    a = -1
    b = 1
    cauchy_distribution_rv = modeling_cauchy_distribution(a, b, n)
    with open("../bin/cauchy_distribution_rc.txt", "w", encoding='utf-8') as file:
        for rv in cauchy_distribution_rv:
            print(rv, file=file)
    print('Распределение Коши:\n\tМатематическое ожидание: {}\t-\t{}'
          .format(expected_value(cauchy_distribution_rv), 'Не определено'))
    print('\tДисперсия: {}\t-\t{}'.format(dispersion(cauchy_distribution_rv), 'Не определена'))
    print('\tКритерий Колмогорова: {}'.format(kolmogorov(cauchy_distribution_rv, cauchy_distribution)))
    print('\tКритерий Пирсона: {}'.format(pearson(cauchy_distribution_rv, cauchy_distribution)))
    res_kolmogorov = 0
    res_pearson = 0
    for i in range(100):
        if not kolmogorov(modeling_cauchy_distribution(a, b, n, primes[i], primes[i]), cauchy_distribution):
            res_kolmogorov += 1
        if not pearson(modeling_cauchy_distribution(a, b, n, primes[i], primes[i]), cauchy_distribution):
            res_pearson += 1
    print('\tВероятность ошибки первого рода(Колмогоров): {}%'.format(res_kolmogorov))
    print('\tВероятность ошибки первого рода(Пирсон): {}%\n'.format(res_pearson))

    a = 2
    b = 3
    logistic_distribution_rv = modeling_logistic_distribution(a, b, n)
    with open("../bin/logistic_distribution_rc.txt", "w", encoding='utf-8') as file:
        for rv in logistic_distribution_rv:
            print(rv, file=file)
    print('Логистическое распределение:\n\tМатематическое ожидание: {}\t-\t{}'
          .format(expected_value(logistic_distribution_rv), a))
    print('\tДисперсия: {}\t-\t{}'.format(dispersion(logistic_distribution_rv), (b * math.pi) ** 2 / 3))
    print('\tКритерий Колмогорова: {}'.format(kolmogorov(logistic_distribution_rv, logistic_distribution)))
    print('\tКритерий Пирсона: {}'.format(pearson(logistic_distribution_rv, logistic_distribution)))
    res_kolmogorov = 0
    res_pearson = 0
    for i in range(100):
        if not kolmogorov(modeling_logistic_distribution(a, b, n, primes[i], primes[i]), logistic_distribution):
            res_kolmogorov += 1
        if not pearson(modeling_logistic_distribution(a, b, n, primes[i], primes[i]), logistic_distribution):
            res_pearson += 1
    print('\tВероятность ошибки первого рода(Колмогоров): {}%'.format(res_kolmogorov))
    print('\tВероятность ошибки первого рода(Пирсон): {}%\n'.format(res_pearson))


if __name__ == '__main__':
    main()
