import copy

from resources import first_matrix, second_matrix, third_matrix, y_axis_for_slae, y_axis_for_inversion
from Matrix import CustomMatrix
import sympy
import numpy
import time
import random
import matplotlib.pyplot as plt


def compute_plot_for_slae() -> list:
    x = [50 * i for i in range(1, 18)]
    y = []
    for dimension in x:
        try:
            matrix = CustomMatrix(generate_matrix(dimension))
            vector = generate_vector(dimension)
            start = time.time()
            matrix.solve_gauss(vector)
            end = time.time()
            y.append(end - start)
        except ZeroDivisionError as e:
            print(e)
    return y


def plot_for_slae():
    x = [50 * i for i in range(1, 18)]
    plt.scatter(x, y_axis_for_slae, color="green")
    plt.xlabel("matrix dimension")
    plt.ylabel("solving time")
    plt.show()


def compute_plot_for_inversion() -> list:
    x = [50 * i for i in range(1, 13)]
    y = []
    for index in range(len(x)):
        try:
            matrix = CustomMatrix(generate_matrix(x[index]))
            start = time.time()
            matrix.inverse()
            end = time.time()
            y.append(end - start)
        except ZeroDivisionError as e:
            print(e)
    return y


def plot_for_inversion():
    x = [50 * i for i in range(1, 13)]
    plt.scatter(x, y_axis_for_inversion, color="green")
    plt.xlabel("matrix dimension")
    plt.ylabel("inversion time")
    plt.show()


def generate_matrix(n: int) -> list:
    generated_matrix = []
    for _ in range(n):
        generated_matrix.append([random.randint(-100, 100) for _ in range(n)])
    return generated_matrix


def generate_vector(n: int) -> list:
    generated_vector = []
    for _ in range(n):
        generated_vector.append(random.randint(-100, 100))
    return generated_vector


def main():
    # First matrix
    matrix = CustomMatrix(copy.deepcopy(first_matrix))
    print("\tFirst matrix:")
    try:
        print(matrix.inverse())
        print("\tExact matrix:")
        exact = sympy.Matrix(copy.deepcopy(first_matrix))
        exact = exact.inv()
        for line in exact.tolist():
            print(line)
        print("\tThe norm of the difference between the exact and approximate matrices: {}"
              .format(numpy.linalg.norm(numpy.subtract(exact.tolist(), matrix.get_matrix()), ord=numpy.inf)))
        print()
    except ZeroDivisionError as e:
        print(e)
        print()

    # Second matrix
    print("\tSecond matrix:")
    matrix = CustomMatrix(copy.deepcopy(second_matrix))
    print(matrix.inverse())
    print("\tExact matrix:")
    exact = sympy.Matrix(copy.deepcopy(second_matrix))
    exact = exact.inv()
    for line in exact.tolist():
        print(line)
    print("\tThe norm of the difference between the exact and approximate matrices: {}"
          .format(numpy.linalg.norm(numpy.subtract(exact.tolist(), matrix.get_matrix()), ord=numpy.inf)))
    print()

    # Third matrix
    print("\tThird matrix:")
    matrix = CustomMatrix(copy.deepcopy(third_matrix))
    print(matrix.inverse())
    print("\tExact matrix:")
    exact = sympy.Matrix(copy.deepcopy(third_matrix))
    exact = exact.inv()
    for line in exact.tolist():
        print(line)
    print("\tThe norm of the difference between the exact and approximate matrices: {}"
          .format(numpy.linalg.norm(numpy.subtract(exact.tolist(), matrix.get_matrix()), ord=numpy.inf)))
    print()


if __name__ == "__main__":
    main()