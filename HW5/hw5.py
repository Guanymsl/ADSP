import numpy as np

def fftreal(f1: np.ndarray, f2: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    N = f1.shape[0]
    f3 = f1.astype(np.complex128) + 1j * f2.astype(np.complex128)
    F3 = np.fft.fft(f3)

    idx = (-np.arange(N)) % N
    F3_conj = np.conjugate(F3[idx])

    F1 = (F3 + F3_conj) / 2
    F2 = (F3 - F3_conj) / (2j)

    return (F1, F2)


if __name__ == "__main__":
    N = 8
    n = np.arange(N)

    f1 = n
    f2 = n[::-1]

    F1_true = np.fft.fft(f1)
    F2_true = np.fft.fft(f2)

    F1_est, F2_est = fftreal(f1, f2)

    print("X_true =", F1_true)
    print("X_est  =", F1_est)
    print("Error X  =", np.max(np.abs(F1_true - F1_est)))

    print("Y_true =", F2_true)
    print("Y_est  =", F2_est)
    print("Error Y  =", np.max(np.abs(F2_true - F2_est)))
