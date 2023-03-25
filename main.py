from random import uniform
import matplotlib.pyplot as plt
from math import floor


def uniform_and_round(a, b, accuracy=2):
    d = 10 ** (-accuracy)
    return round(uniform(a - d, b + d), accuracy)


def X_density(x):  # плотность X
    if x <= 1 or x > 2:
        return 0
    return 3 * (x - 1) ** 2


def get_random_X(accuracy=6):  # получение случайного X
    X = uniform_and_round(1, 2, accuracy=accuracy)
    p = uniform(0, 1)
    if p < X_density(X):
        return X
    return get_random_X()


# Функция генерирующая много случайных величин
def get_values(func, n=10 ** 6):
    for i in range(n):
        p = func()
        yield p


# Функция получения словаря {значение: частота}
def get_frequency_dict(func, density, n=10 ** 6, accuracy=2):
    d = {}
    for val in get_values(func, n):
        val = round(val, 2)
        if density(val) <= 0:
            continue
        if val in d:
            d[val] += 1
        else:
            d[val] = 1
    return d


def get_x_y_arr_from_dict(d):
    items = sorted(d.items())
    return [i[0] for i in items], [i[1] for i in items]


def plot(func, density):
    d = get_frequency_dict(func, density)
    x, y = get_x_y_arr_from_dict(d)
    plt.plot(x, y)
    plt.show()


get_random_X()
