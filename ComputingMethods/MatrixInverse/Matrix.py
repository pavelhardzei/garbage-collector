import copy
import math


class CustomMatrix:
    def __init__(self, matrix: list):
        self.__matrix = matrix

    def get_matrix(self) -> list:
        return self.__matrix

    def get_matrix_dimension(self) -> int:
        return len(self.__matrix)

    def set_matrix(self, matrix: list):
        self.__matrix = matrix

    def inverse(self):
        if not self.__check_if_square_matrix():
            raise Exception("Matrix is not square.")

        size = len(self.__matrix)
        identity_matrix = [size * [0] for _ in range(size)]
        for i in range(size):
            identity_matrix[i][i] = 1

        for i in range(size - 1):
            self.__choose_max(identity_matrix, i)
            for j in range(i + 1, size):
                self.__update_line(identity_matrix, i, j)

        for l in range(size):
            for i in range(size - 1, -1, -1):
                summa = 0
                for j in range(i + 1, size):
                    summa += self.__matrix[i][j] * identity_matrix[j][l]
                identity_matrix[i][l] -= summa
                identity_matrix[i][l] /= self.__matrix[i][i]

        self.__matrix = identity_matrix
        return self

    def solve_gauss(self, vector: list) -> list:
        if not self.__check_if_square_matrix():
            raise Exception("Matrix is not square.")
        if len(self.__matrix) != len(vector):
            raise Exception("Invalid length of vector.")

        result = copy.deepcopy(vector)
        matrix = copy.deepcopy(self.__matrix)
        size = len(self.__matrix)

        for i in range(size - 1):
            self.__choose_max(result, i)
            for j in range(i + 1, size):
                self.__update_line(vector=result, base_line_index=i, row=j)

        for i in range(size - 1, -1, -1):
            summa = 0
            for j in range(i + 1, size):
                summa += self.__matrix[i][j] * result[j]
            result[i] -= summa
            result[i] /= self.__matrix[i][i]

        self.__matrix = matrix
        return result

    def __check_if_square_matrix(self) -> bool:
        for line in self.__matrix:
            if len(line) != len(self.__matrix):
                return False
        return True

    def __choose_max(self, matrix_or_vector: list, row: int):
        res_row = row
        max_element = math.fabs(self.__matrix[row][row])
        for i in range(row + 1, len(self.__matrix)):
            if math.fabs(self.__matrix[i][row]) > max_element:
                max_element = math.fabs(self.__matrix[i][row])
                res_row = i
        self.__matrix[row], self.__matrix[res_row] = self.__matrix[res_row], self.__matrix[row]
        matrix_or_vector[row], matrix_or_vector[res_row] = matrix_or_vector[res_row], matrix_or_vector[row]

    def __update_line(self, identity_matrix: list = None, base_line_index: int = 0, row: int = 0,
                      vector: list = None):
        if self.__matrix[base_line_index][base_line_index] == 0:
            raise ZeroDivisionError("Matrix is not invertible: determinant is equal to zero.")
        l = -self.__matrix[row][base_line_index] / self.__matrix[base_line_index][base_line_index]
        for col in range(base_line_index, len(self.__matrix)):
            self.__matrix[row][col] += l * self.__matrix[base_line_index][col]
        if identity_matrix is not None:
            for col in range(len(self.__matrix)):
                identity_matrix[row][col] += l * identity_matrix[base_line_index][col]
        if vector is not None:
            vector[row] += l * vector[base_line_index]

    def __str__(self):
        lines = ''
        for line in self.__matrix:
            lines += str([round(x, 10) for x in line]) + "\n"
        return lines