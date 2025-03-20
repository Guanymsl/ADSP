import numpy as np
import matplotlib.pyplot as plt
import random

N = 19
k = (N - 1) // 2

fs = 8000.0
fstop = 2200.0
bw = 200.0

delta = 0.0001

d = 0.00001
r = 5
D = 50001

def initial_F():
    interval1 = (0, (fstop - bw) / fs)
    interval2 = ((fstop + bw) / fs, 0.5)

    n1 = random.randint(1, k + 1)
    n2 = k + 2 - n1

    iniF1 = [round(random.uniform(interval1[0], interval1[1]), r) for _ in range(n1)]
    iniF2 = [round(random.uniform(interval2[0], interval2[1]), r) for _ in range(n2)]

    iniF = iniF1 + iniF2
    iniF.sort(key=lambda x: x)

    return iniF

def w(_F):
    if _F >= 0 and _F <= (fstop - bw) / fs:
        return 0.6
    if _F >= (fstop - bw) / fs and _F <= (fstop + bw) / fs:
        return 0
    return 1

def H_d(_F):
    if _F >= 0 and _F <= fstop / fs:
        return 0
    return 1

def calculate_s(_F):
    A = np.zeros((k + 2, k + 2))
    H = np.zeros(k + 2)

    for i in range(k + 2):
        for j in range(k + 1):
            A[i][j] = np.cos(2 * np.pi * _F[i] * j)

        A[i][k + 1] = (-1) ** i / w(_F[i])
        H[i] = H_d(_F[i])

    s = np.linalg.inv(A) @ H
    return s

def calculate_err(_s):
    err = np.zeros(D)

    for i in range(D):
        sum = 0
        for j in range(k + 1):
            sum += _s[j] * np.cos(2 * np.pi * i * d * j)
        err[i] = (sum - H_d(i * d)) * w(i * d)

    return err

def choose_F(_err):
    newF = []
    maxE = abs(_err[0])

    if (_err[0] > 0 and _err[0] > _err[1]) or (_err[0] < 0  and _err[0] < _err[1]):
            newF.append((0, abs(_err[0])))

    for i in range(1, D - 1):
        maxE = max(maxE, abs(_err[i]))
        if (_err[i] > _err[i - 1]  and _err[i] > _err[i + 1]) or (_err[i] < _err[i - 1]  and _err[i] < _err[i + 1]):
            newF.append((i, abs(_err[i])))

    if (_err[D - 1] > 0  and _err[D - 1] > _err[D - 2]) or (_err[D - 1] < 0  and _err[D - 1] < _err[D - 2]):
            newF.append((D - 1, abs(_err[D - 1])))

    newF.sort(key = lambda x: -x[1])
    newF = newF[:k + 2]
    newF.sort(key = lambda x: x[0])
    newF = [x[0] * d for x in newF]
    return newF, maxE

if "__main__" == __name__:
    s = np.zeros(k + 2)
    # F = [0, 0.05, 0.1, 0.15, 0.2, 0.24, 0.31, 0.35, 0.4, 0.45, 0.5]
    F = initial_F()
    E = []

    prevE = np.inf
    while True:
        s = calculate_s(F)
        err = calculate_err(s)
        F, curE = choose_F(err)
        E.append(curE)
        if prevE - curE >= 0 and prevE - curE <= delta:
            break
        prevE = curE

    RF = []
    for f in F:
        sum = 0
        for n in range(k + 1):
            sum += s[n] * np.cos(2 * np.pi * n * f)
        RF.append(sum)

    h = np.zeros(N)
    h[k] = s[0]
    for n in range(1, k + 1):
        h[k + n] = s[n] / 2
        h[k - n] = s[n] / 2

    plt.figure(figsize=(10, 6))
    plt.plot(F, RF, color='orange')
    plt.title("Frequency Response")
    plt.xlabel("Normalized Frequency")
    plt.ylabel("Amplitude")
    plt.grid(True)

    plt.figure(figsize=(10, 6))
    plt.plot(E, color='green')
    plt.title("Maximal Error")
    plt.xlabel("Iteration")
    plt.ylabel("$E_0$")
    plt.xticks(np.arange(len(E)))
    plt.grid(True)

    plt.figure(figsize=(10, 6))
    plt.stem(range(len(h)), h, linefmt='magenta', markerfmt='o', basefmt='black')
    plt.title("Impulse Response")
    plt.xlabel("n")
    plt.ylabel("$h[n]$")
    plt.xticks(np.arange(len(h)))

    plt.show()
