from random import randrange, uniform

import numpy as np

from base_func import BaseFunction
from math import log, ceil


class RandomVariable:
    def __init__(self, density_func=None, distribution_func=None, random_variable_func=None):
        # добавить область где вероятность меняется
        self.max_density_value = 0
        self.__ideal_density_func = density_func
        self.__distribution_func = distribution_func
        self.__random_variable_func = random_variable_func
        
        if density_func is None and distribution_func is None and random_variable_func is None:
            raise ValueError("At least one of density_func, distribution_func, or random_variable_func must be defined.")
        
        self.__statistics_density_func = None
        self.__statistics_distribution_func = None
        self.__statistics_random_variable_func = None

        self.__statistics_density_func_defined = False
        self.__statistics_distribution_func_defined = False
        self.__statistics_random_variable_func_defined = False

        # Можно все эти подсчеты сделать ленивыми
        # if not self.ideal_density_func_defined():
        #     self.count_statistics_density_func()
        # self.max_density_value = self.get_max_density_value()
        #
        # if not self.ideal_distribution_func_defined():
        #     self.count_statistics_distribution_func()
        # if not self.ideal_random_variable_func_defined():
        #     self.count_statistics_random_value_func()

    def get_max_density_value(self, start_x=-100, end_x=100, accuracy=0.01): # Здесь потом можно использовать область определения
        maxx = 0
        for x in np.arange(start_x, end_x + accuracy * 10 ** -5, accuracy):
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

        self.__statistics_density_func = lambda x, d=0.001: \
            (self.distribution_func(x + d / 2) - self.distribution_func(x - d / 2)) / d
    
    def count_statistics_distribution_func(self, iterations=10**6, accuracy=0.01):
        if self.ideal_distribution_func_defined():
            print('Warning: counting statistics distribution when ideal distribution is defined.')
        if not self.random_variable_func_defined():
            self.count_statistics_random_value_func()

        # print(r.random_variable_func(), r.random_variable_func())
        random_values = sorted([self.random_variable_func() for _ in range(iterations)])
        # print(random_values)
        d = dict()

        print(random_values)

        d[random_values[0]] = 1
        for i in range(1, len(random_values)):
            if random_values[i] - random_values[i - 1] < accuracy: # устранить погрешность в максимальных значениях
                random_values[i] = random_values[i - 1]

            if random_values[i] not in d:
                d[random_values[i]] = 1
            else:
                d[random_values[i]] += 1

        rounding_decimal_places = ceil(-log(10, accuracy))
        for i in d.keys():
            d[i] /= iterations
            d[i] = round(d[i], rounding_decimal_places)

        self.__statistics_distribution_func = lambda x: d[round(x, rounding_decimal_places)]\
            if round(x, rounding_decimal_places) in d else 0

    def count_statistics_random_value_func(self, start=-100, end=100):
        if self.ideal_random_variable_func_defined():
            print('Warning: counting statistics random value when ideal random variable is defined.')
        if not self.density_func_defined():
            self.count_statistics_density_func()

        def f():
            x = uniform(start, end)
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
    r = RandomVariable(density_func=lambda x: 2 * x if 0 <= x <= 1 else 0)
    r.max_density_value = r.get_max_density_value(0, 3, accuracy=10**-6)
    r.count_statistics_random_value_func(start=0, end=2)
    r.count_statistics_distribution_func(iterations=10)
    print(r.density_func_defined(), r.ideal_density_func_defined(), r.statics_density_func_defined())
    print(r.max_density_value)

    # BaseFunction(r.density_func).plot(-5, 5, accuracy=0.1)
    # BaseFunction(r.distribution_func).plot(-5, 5, accuracy=0.1)
    # print(sorted([r.random_variable_func() for i in range(1000)]))





