import copy
import numpy as np


class Slae:
    def __init__(self, A: list[list], b: list):
        self.__A = copy.deepcopy(A)
        self.__b = copy.deepcopy(b)
        if not self.__isSquare() or len(A) != len(b):
            raise Exception("Invalid input")

    def relaxation(self, w: float = 1.0, k: int = 3, init: list = None) -> list:
        e = 10 ** (-k)
        size = len(self.__b)
        if init is not None:
            if len(init) != size:
                raise Exception("Invalid input")
            x = copy.deepcopy(init)
        else:
            x = size * [0.0]
        x_next = size * [0.0]

        while np.linalg.norm(np.subtract(np.matmul(self.__A, x), self.__b), np.inf) > e:
            for i in range(size):
                sum1 = sum2 = 0.0
                for j in range(i):
                    sum1 += self.__A[i][j] * x_next[j]
                for j in range(i + 1, size):
                    sum2 += self.__A[i][j] * x[j]
                x_next[i] = (1 - w) * x[i] + (w / self.__A[i][i]) * (self.__b[i] - sum1 - sum2)
            x = x_next
            x_next = size * [0.0]

        return x

    @staticmethod
    def sparse_slae(main_diagonal: list, side_diagonal: list, b: list, k: int = 3, init: list = None) -> list:
        if len(main_diagonal) != len(side_diagonal) or len(main_diagonal) != len(b) or len(b) % 2 != 0:
            raise Exception("The size must be even")

        e = 10 ** (-k)
        size = len(b)
        if init is not None:
            if len(init) != size:
                raise Exception("Invalid input")
            x = copy.deepcopy(init)
        else:
            x = size * [10.0]
        x_next = size * [0.0]

        while np.linalg.norm(np.subtract(Slae.sparse_dot(main_diagonal, side_diagonal, x), b), np.inf) > e:
            for i in range(size):
                summa: float
                if i < size // 2:
                    summa = side_diagonal[i] * x[size - 1 - i]
                else:
                    summa = side_diagonal[i] * x_next[size - 1 - i]
                x_next[i] = (b[i] - summa) / main_diagonal[i]
            x = x_next
            x_next = size * [0.0]

        return x

    def __isSquare(self) -> bool:
        for line in self.__A:
            if len(line) != len(self.__A):
                return False
        return True

    @staticmethod
    def sparse_dot(main_diagonal: list, side_diagonal: list, x: list) -> list:
        if len(main_diagonal) != len(side_diagonal) or len(main_diagonal) != len(x) or len(x) % 2 != 0:
            raise Exception("The size must be even")
        size = len(x)
        res = size * [0]
        for i in range(size):
            res[i] = main_diagonal[i] * x[i] + side_diagonal[i] * x[size - 1 - i]
        return res