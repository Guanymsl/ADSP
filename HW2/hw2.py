import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import freqz

def H(F):
    return 1j * 2 * np.pi * F

if __name__ == "__main__":
    k = int(input("Enter a value for k: "))
    N = 2 * k + 1
    Hd = np.zeros(N, dtype=complex)

    for i in range(N):
        if i / N < 0.5:
            Hd[i] = H(i / N)
        else:
            Hd[i] = H(i / N - 1)

    Hd[k] = 0.7 * Hd[k]
    Hd[k + 1] = 0.7 * Hd[k + 1]

    r1 = np.real(np.fft.ifft(Hd))
    h = np.concatenate((r1[k + 1:], r1[:k + 1]))

    w, RF = freqz(h, worN=8000, whole=True)
    RF = RF * np.exp(1j * w * k)

    plt.figure(figsize=(10, 6))
    plt.stem(range(len(h)), h, linefmt='magenta', markerfmt='o', basefmt='black')
    plt.title("Impulse Response")
    plt.xlabel("n")
    plt.ylabel("$h[n]$")
    plt.xticks(np.arange(len(h)))

    plt.figure(figsize=(10, 6))
    plt.plot(w / (2 * np.pi), RF.imag, color='orange')
    plt.title("Imaginary Part of Frequency Response")
    plt.xlabel("Normalized Frequency")
    plt.ylabel("Amplitude")
    plt.grid(True)

    plt.show()
