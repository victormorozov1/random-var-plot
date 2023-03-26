import bisect
from importlib.metadata import distribution
from random import randrange, uniform

import numpy as np
from matplotlib import pyplot as plt

from base_func import BaseFunction
from math import log, ceil, floor

import bisect
from random import randrange, uniform

import numpy as np
from matplotlib import pyplot as plt

from math import log, ceil, floor


class RandomVariable:
    def __init__(self, min_random_value, max_random_value, density_func=None, distribution_func=None,
                 random_variable_func=None):
        # добавить область где вероятность меняется
        self.__distribution_func_values = None

        self.max_density_value = 0
        self.__ideal_density_func = density_func
        self.__distribution_func = distribution_func
        self.__random_variable_func = random_variable_func

        if density_func is None and distribution_func is None and random_variable_func is None:
            raise ValueError(
                "At least one of density_func, distribution_func, or random_variable_func must be defined.")

        self.__statistics_density_func = None
        self.__statistics_distribution_func = None
        self.__statistics_random_variable_func = None

        self.__statistics_density_func_defined = False
        self.__statistics_distribution_func_defined = False
        self.__statistics_random_variable_func_defined = False

        self.min_random_value, self.max_random_value = min_random_value, max_random_value

    def count_all(self, distribution_iterations=10**5, distribution_accuracy=0.01, counting_density_max_accuracy=10**-4):
        # Можно все эти подсчеты сделать ленивыми
        if not self.ideal_density_func_defined():
            self.count_statistics_density_func()
        self.max_density_value = self.get_max_density_value(accuracy=counting_density_max_accuracy)

        if not self.ideal_distribution_func_defined():
            self.count_statistics_distribution_func(iterations=distribution_iterations, accuracy=distribution_accuracy)
        if not self.ideal_random_variable_func_defined():
            self.count_statistics_random_value_func()

    def get_max_density_value(self, accuracy=0.01):  # Здесь потом можно использовать область определения
        maxx = 0
        for x in np.arange(self.min_random_value, self.max_random_value + accuracy * 10 ** -5, accuracy):
            if self.density_func(x) > maxx:
                maxx = self.density_func(x)
        return maxx

    def ideal_density_func_defined(self):
        return self.__ideal_density_func is not None

    def ideal_distribution_func_defined(self):
        return self.__distribution_func is not None

    def ideal_random_variable_func_defined(self):
        return self.__random_variable_func is not None

    def statics_density_func_defined(self):
        return self.__statistics_density_func_defined

    def statics_distribution_func_defined(self):
        return self.__statistics_distribution_func_defined

    def statics_random_variable_func_defined(self):
        return self.__statistics_random_variable_func_defined

    def density_func_defined(self):
        return self.statics_density_func_defined() or self.ideal_density_func_defined()

    def distribution_func_defined(self):
        return self.statics_distribution_func_defined() or self.ideal_distribution_func_defined()

    def random_variable_func_defined(self):
        return self.statics_random_variable_func_defined() or self.ideal_random_variable_func_defined()

    def density_func(self, x):
        if self.ideal_density_func_defined():
            return self.__ideal_density_func(x)
        return self.__statistics_density_func(x)

    def distribution_func(self, x):
        if self.ideal_distribution_func_defined():
            return self.__distribution_func(x)
        return self.__statistics_distribution_func(x)

    def random_variable_func(self):
        if self.ideal_random_variable_func_defined():
            return self.__random_variable_func()
        return self.__statistics_random_variable_func()

    def count_statistics_density_func(self):
        if self.ideal_density_func_defined():
            print('Warning: counting statistics density when ideal density is defined.')
        if not self.distribution_func_defined():
            self.count_statistics_distribution_func()

        def f(x, d=0.1):
            derivative = (self.distribution_func(x + d / 2) - self.distribution_func(x - d / 2)) / d
            if abs(derivative) > 200:  # Костыль. Нужно бы нормально сделать
                return 0
            return derivative

        self.__statistics_density_func = f

    def count_statistics_distribution_func(self, iterations=10 ** 6, accuracy=0.01):
        if self.ideal_distribution_func_defined():
            print('Warning: counting statistics distribution when ideal distribution is defined.')
        if not self.random_variable_func_defined():
            self.count_statistics_random_value_func()

        random_values = sorted([self.random_variable_func() for _ in range(iterations)])
        d = dict()

        d[random_values[0]] = 1
        for i in range(1, len(random_values)):
            if random_values[i] - random_values[i - 1] < accuracy:  # устранить погрешность в максимальных значениях
                random_values[i] = random_values[i - 1]

            if random_values[i] not in d:
                d[random_values[i]] = 1
            else:
                d[random_values[i]] += 1

        self.__distribution_func_values = sorted(d.items())
        #         Почемут сюда я захожу 2 раза
        for i in range(len(self.__distribution_func_values)):
            self.__distribution_func_values[i] = list(self.__distribution_func_values[i])
            if i >= 1:
                self.__distribution_func_values[i][1] = self.__distribution_func_values[i][1] / iterations + \
                                                        self.__distribution_func_values[i - 1][1]
            else:
                self.__distribution_func_values[i][1] = self.__distribution_func_values[i][1] / iterations

        def f(x):
            # print(self.__distribution_func_values)
            x_arr = [i[0] for i in self.__distribution_func_values]
            y_arr = [i[0] for i in self.__distribution_func_values]
            x1_ind, x2_ind = bisect.bisect_left(x_arr, x), bisect.bisect_right(x_arr, x)
            if x1_ind >= len(x_arr):
                x1_ind = len(x_arr) - 1
            if x2_ind >= len(x_arr):
                x2_ind = len(x_arr) - 1
            x1, y1 = x_arr[x1_ind], y_arr[x1_ind]
            x2, y2 = x_arr[x2_ind], y_arr[x2_ind]
            if abs(x - x2) > 0.1:  # Написать бы нормально через accuracy
                return self.__distribution_func_values[x1_ind][1]
            if abs(x - x1) < abs(x - x2):
                return self.__distribution_func_values[x1_ind][1]
            return self.__distribution_func_values[x2_ind][1]

        self.__statistics_distribution_func = f

    def count_statistics_random_value_func(self):
        if self.ideal_random_variable_func_defined():
            print('Warning: counting statistics random value when ideal random variable is defined.')
        if not self.density_func_defined():
            self.count_statistics_density_func()

        def f():
            x = uniform(self.min_random_value, self.max_random_value)
            # print('x =', x)
            p = uniform(0, self.max_density_value)
            if p < self.density_func(x):
                return x
            return f()

        self.__statistics_random_variable_func = f

    def ideal_density_func(self, x):
        if self.ideal_density_func_defined():
            return self.__ideal_density_func(x)
        raise ValueError("No density function defined.")

    def ideal_distribution_func(self, x):
        if self.ideal_distribution_func_defined():
            return self.__distribution_func(x)
        raise ValueError("No distribution function defined.")

    def ideal_random_variable_func(self):
        if self.ideal_random_variable_func_defined():
            return self.__random_variable_func()
        raise ValueError("No random variable function defined.")

    def statics_density_func(self, x):
        if self.statics_density_func_defined():
            return self.__statistics_density_func(x)
        raise ValueError("No statistics density function defined.")

    def statics_distribution_func(self, x):
        if self.statics_distribution_func_defined():
            return self.__statistics_distribution_func(x)
        raise ValueError("No statistics distribution function defined.")

    def statics_random_variable_func(self):
        if self.statics_random_variable_func_defined():
            return self.__statistics_random_variable_func()
        raise ValueError("No statistics random variable function defined.")


if __name__ == '__main__':
    def rv():
        if randrange(0, 2) == 0:
            return 6
        return uniform(5, 7)
    r = RandomVariable(0, 7, random_variable_func=rv)
    r.count_all(distribution_accuracy=0.1, distribution_iterations=10 ** 4, counting_density_max_accuracy=0.01)

    BaseFunction(r.distribution_func).plot(0, 8, accuracy=0.01)
    BaseFunction(r.density_func).plot(0, 8, accuracy=0.01)
    # BaseFunction(r.distribution_func).plot(-5, 5, accuracy=0.1)
    plt.show()
    # print(sorted([r.random_variable_func() for i in range(1000)]))
