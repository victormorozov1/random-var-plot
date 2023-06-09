import matplotlib.pyplot as plt
import numpy as np

# Клас кажется слишком сложно для такой задачи. МОжно в функцю переделать
class BaseFunction:
    def __init__(self, func):
        self.func = func
        # можно добавить область определения

    def get_x_y_arrs(self, x_start, x_end, accuracy=0.1):
        x, y = [], []
        for i in np.arange(x_start, x_end + min(accuracy, 1), accuracy):
            x.append(i)
            y.append(self.func(i))
        return x, y

    def plot(self, x_start, x_end, accuracy=0.1):
        x, y = self.get_x_y_arrs(x_start, x_end, accuracy)
        plt.plot(x, y)
        # plt.show()


if __name__ == '__main__':
    f = BaseFunction(lambda x: 2 * x if 0 <= x < 2 else 6)
    f.plot(-10, 10, accuracy=0.1)
