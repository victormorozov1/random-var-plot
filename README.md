# Построение графиков случайных величин
Данная программа может восстановить и построить функцию/ее плотность/функцию распределения имея на входе хотя-бы одну из трех перечисленных вещей.

Например задав функцию случайной переменной вы можете восстановить ее плотность и функцию распределения:

```python
def rv():
    if randrange(0, 2) == 0:  # Случайная переменная
        return uniform(0, 4) / 2
    return uniform(0, 2)
    
r = RandomVariable(0, 7, random_variable_func=rv)
r.count_all(distribution_accuracy=0.1, distribution_iterations=10 ** 2, counting_density_max_accuracy=0.01)

BaseFunction(r.distribution_func).plot(0, 3, accuracy=0.001)  # Строим функцию распределения
BaseFunction(r.density_func).plot(0, 3, accuracy=0.001)  # Строим функцию плотности
plt.show()
```

![image](https://user-images.githubusercontent.com/33213745/233858419-b4e7ec3e-372e-454b-a94a-3a72ea66ec3c.png)
