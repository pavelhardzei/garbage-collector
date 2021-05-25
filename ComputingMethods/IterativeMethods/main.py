import numpy as np
import copy
import time
from matplotlib import pyplot as plt
from Slae import Slae

# counted using function get_time_for_n
dimensions = [4, 10, 32, 100, 316, 1000, 3162, 10000, 31622, 100000, 316228, 1000000]
time_list = [0.0, 0.0, 0.0, 0.0, 0.015624761581420898, 0.015623092651367188,
             0.12499880790710449, 0.29686474800109863, 0.968719482421875,
             3.2186429500579834, 9.452810525894165, 29.81579041481018]


def count_discrepancy_norms_task2(A: list[list], b: list, w: float = 1.0, k: int = 100, init: list = None) -> list:
    discrepancy_norms = []
    size = len(b)
    if init is not None:
        if len(init) != size:
            raise Exception("Invalid input")
        x = copy.deepcopy(init)
    else:
        x = size * [0.0]
    x_next = size * [0.0]

    for _ in range(k):
        discrepancy_norms.append(np.linalg.norm(np.subtract(np.matmul(A, x), b), np.inf))
        for i in range(size):
            sum1 = sum2 = 0.0
            for j in range(i):
                sum1 += A[i][j] * x_next[j]
            for j in range(i + 1, size):
                sum2 += A[i][j] * x[j]
            x_next[i] = (1 - w) * x[i] + (w / A[i][i]) * (b[i] - sum1 - sum2)
        x = x_next
        x_next = size * [0.0]

    return discrepancy_norms


def convergence_diagram_task2(A: list[list], b: list, k: int):
    d1 = count_discrepancy_norms_task2(A, b, 0.5, k)
    d2 = count_discrepancy_norms_task2(A, b, 1.9, k)
    d3 = count_discrepancy_norms_task2(A, b, 1, k)
    d4 = count_discrepancy_norms_task2(A, b, 0.1, k)
    d5 = count_discrepancy_norms_task2(A, b, 1.7, k)
    x = list(range(1, k + 1))
    ax = plt.subplots()[1]
    ax.plot(x, d1, color='blue')
    ax.plot(x, d2, color='orange')
    ax.plot(x, d3, color='green')
    ax.plot(x, d4, color='cyan')
    ax.plot(x, d5, color='red')
    ax.set_xlabel('iterations')
    ax.set_ylabel('discrepancy norm')
    ax.set_yscale('log')
    ax.set_xscale('log')
    plt.title('Initial approximation: [0.0, 0.0, 0.0]')
    plt.legend(["w = 0.5", "w = 1.9", "w = 1", "w = 0.1", "w = 1.7"], loc='lower right')
    plt.show()


def count_discrepancy_norms_task5(main_diagonal: list,
                                  side_diagonal: list, b: list, k: int = 100, init: list = None):
    if len(main_diagonal) != len(side_diagonal) or len(main_diagonal) != len(b) or len(b) % 2 != 0:
        raise Exception("The size must be even")

    size = len(b)
    discrepancy_norms = []
    if init is not None:
        if len(init) != size:
            raise Exception("Invalid input")
        x = copy.deepcopy(init)
    else:
        x = size * [10.0]
    x_next = size * [0.0]

    for _ in range(k):
        discrepancy_norms.append(np.linalg.norm
                                 (np.subtract(Slae.sparse_dot(main_diagonal, side_diagonal, x), b), np.inf))
        for i in range(size):
            summa: float
            if i < size // 2:
                summa = side_diagonal[i] * x[size - 1 - i]
            else:
                summa = side_diagonal[i] * x_next[size - 1 - i]
            x_next[i] = (b[i] - summa) / main_diagonal[i]
        x = x_next
        x_next = size * [0.0]

    return discrepancy_norms


def convergence_diagram_task5(k: int):
    d1 = count_discrepancy_norms_task5([3 for _ in range(100)], [-2 for _ in range(100)], [1 for _ in range(100)], k)
    d2 = count_discrepancy_norms_task5([3 for _ in range(1000)], [-2 for _ in range(1000)], [1 for _ in range(1000)], k)
    d3 = count_discrepancy_norms_task5([3 for _ in range(10000)], [-2 for _ in range(10000)], [1 for _ in range(10000)], k)
    x = list(range(1, k + 1))
    plt.plot(x, d1, lw=10)
    plt.plot(x, d2, lw=5)
    plt.plot(x, d3)
    plt.xlabel('iterations')
    plt.ylabel('discrepancy norm')
    plt.legend(["n = 100", "n = 1000", "n = 10000"], loc='upper right')
    plt.title('Initial approximation: [10.0, 10.0, 10.0]')
    plt.show()


def get_time_for_n():
    time_arr = []
    n = [int(10 ** (k / 2)) for k in range(1, 13)]
    n = list(map(lambda x: x + 1 if x % 2 != 0 else x, n))
    for s in n:
        start = time.time()
        Slae.sparse_slae([3 for _ in range(s)], [-2 for _ in range(s)], [1 for _ in range(s)], 8)
        time_arr.append(time.time() - start)
    return n, time_arr


def time_diagram(n, time_arr):
    plt.plot(n, time_arr)
    plt.xlabel('dimension')
    plt.ylabel('convergence time in sec')
    plt.title('Initial approximation: [0.0, 0.0, 0.0]')
    plt.show()


def main():
    print("Задание 2\n")
    A = [
        [-1, 1, -1],
        [-1, 4, -2],
        [2, -3, 5]
    ]
    b = [-1, 1, 4]
    print("Матрица:\n", A, "\nВектор b:\n", b)
    print("\n\nСходится при w = 0.5:")
    slae = Slae(A, b)
    print(slae.relaxation(w=0.5, k=5))
    print("\n\nНе сходится при w = 1.9:")
    np.seterr(all='print')
    print(slae.relaxation(w=1.9, k=5))
    convergence_diagram_task2(A, b, 1000)

    print("Задание 5\n")
    print("Матрица вида:\n")
    print([[3, 0, 0, -2], [0, 3, -2, 0], [0, -2, 3, 0], [-2, 0, 0, 3]])
    print("Где n - четное\n", "Вектор b:\n", [1, 1, 1, 1])
    print("\nРезультат:")
    for s in range(6, 11, 2):
        print(Slae.sparse_slae([3 for _ in range(s)], [-2 for _ in range(s)], [1 for _ in range(s)]))
    convergence_diagram_task5(50)
    time_diagram(dimensions, time_list)


if __name__ == "__main__":
    main()