"""4 Kyu rank
# https://www.codewars.com/kata/5a3af5b1ee1aaeabfe000084
"""

import numpy as np
import functools as ft
import itertools as it
import copy


def replace(xs, i, val):
    _xs = xs.copy()
    _xs[i] = val
    return _xs


def max_knapsack(values, weights, W_max):
    v = values
    w = weights
    n = len(values)
    z = [0] * n

    def aux(i, lim_sup, res):
        if i < 0:
            return res, 0
        elif w[i] > lim_sup:
            return aux(i - 1, lim_sup, res)
        else:
            r_left, left = aux(i - 1, lim_sup, res)
            r_right, right = aux(i - 1, lim_sup - w[i], replace(res, i, 1))
            if left <= right + v[i]:
                return r_right, (right + v[i])
            else:
                return r_left, left

    return aux(n - 1, W_max, z)


def min_knapsack(values, weights, W_min):
    v = values
    w = weights
    n = len(values)
    res = [0] * n

    def aux(i, lim_inf):
        if lim_inf < 0:
            return 0
        if i == 0:
            return np.inf
        else:
            k = w[i] - lim_inf
            left = aux(i - 1, lim_inf)
            right = aux(i - 1, k) + v[i]
            if left >= right and k >= W_min:
                res[i] = 1
                return right
            else:
                res[i] = 0
                return left

    return res, aux(n - 1, 2)


def naive_knapsack(_values, _weights, W_max):
    values = np.array(_values)
    weights = np.array(_weights)
    n = len(values)
    xs = it.product({0, 1}, repeat=n)
    profits = (
        (np.dot(values, np.array(x)), np.dot(weights, np.array(x)), x) for x in xs
    )
    return max(filter(lambda x: x[1] <= W_max, profits), key=lambda x: x[0])


if __name__ == "__main__":
    weights = [1, 2, 3, 5]
    values = [1, 6, 10, 16]
    print(naive_knapsack(values, weights, 7))
    print(naive_knapsack(values, weights, 6))

    print(max_knapsack(values, weights, 7))
    print(max_knapsack(values, weights, 6))
