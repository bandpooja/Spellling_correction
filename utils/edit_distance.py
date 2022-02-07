import numpy as np


def levenshtein(token1, token2, print_: bool = False):
    distances = np.zeros((len(token1) + 1, len(token2) + 1))
    for t1 in range(len(token1) + 1):
        distances[t1][0] = t1
    for t2 in range(len(token2) + 1):
        distances[0][t2] = t2

    for t1 in range(1, len(token1) + 1):
        for t2 in range(1, len(token2) + 1):
            a = distances[t1][t2 - 1]
            b = distances[t1 - 1][t2]
            c = distances[t1 - 1][t2 - 1]

            if a <= b and a <= c:
                distances[t1][t2] = a + 1
            elif b <= a and b <= c:
                distances[t1][t2] = b + 1
            else:
                if token1[t1 - 1] == token2[t2 - 1]:
                    distances[t1][t2] = c
                else:
                    distances[t1][t2] = c + 2

    if print_:
        print(f'distance matrix b/w : {token1} and {token2}')
        print_matrix(distances, len(token1), len(token2))
        print('\n')
    return int(distances[len(token1)][len(token2)])


def print_matrix(distances, token1Length, token2Length):
    for t1 in range(token1Length + 1):
        for t2 in range(token2Length + 1):
            print(int(distances[t1][t2]), end=" ")
        print()
