from scipy.optimize import curve_fit
from random import random


def f(x, a, b, c):
    return b * (x**a) + c


r = [f(i, 3, 10, 2) + 0.2 * random() for i in range(5)]

# print(r)
p1, p2 = curve_fit(f, xdata=range(5), ydata=r)

print(p1)
