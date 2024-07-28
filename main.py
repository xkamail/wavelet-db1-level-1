import numpy as np
from matplotlib import pyplot as plt

def db4_detail_coefficients(x):
    # symmetric
    # ... x2 x1 | x1 x2 ... xn | xn xn-1 ...
    symmetric = np.zeros(len(x)*2)
    for n in range(len(x)):
        symmetric[2*n] = x[n]
        symmetric[2*n+1] = x[n]
    x = symmetric
    d = np.zeros(len(x)//2)
    for n in range(len(d)):
        for k in range(4):
            if 2*n-k < 0:
                continue
            if 2*n-k > len(x):
                continue
            d[n] += g[k] * x[2*n-k]
    return d

def differiator(x,scale=1):
    d = np.zeros(len(x))
    for n in range(len(x)):
        d[n] = scale*(x[n] - x[n-1])
    return d

def high_pass_filter(x):
    # y[n]=α⋅(y[n−1]+x[n]−x[n−1])
    y = np.zeros(len(x))
    alpha = 0.895
    print("apply high_pass_filter with alpha: ", alpha)
    for n in range(len(x)):
        y[n] = alpha * (y[n-1] + x[n] - x[n-1])
    return y

def low_pass_filter(x):
    # y[n]=α⋅(y[n−1]+x[n])
    y = np.zeros(len(x))
    alpha = 0.105
    print("apply low_pass_filter with alpha: ", alpha)
    for n in range(len(x)):
        y[n] = alpha * (y[n-1] + x[n])
    return y

m = np.genfromtxt('m.csv', delimiter=',')
# scaling coefficients
h = [
    (1+np.sqrt(3))/(4*np.sqrt(2)),
    (3+np.sqrt(3))/(4*np.sqrt(2)),
    (3-np.sqrt(3))/(4*np.sqrt(2)),
    (1-np.sqrt(3))/(4*np.sqrt(2)),
]
# wavelet coefficients
g=[h[3], -h[2], h[1], -h[0]]

# plt.plot(m[:], label='original')
# plt.plot(high_pass_filter(m), label='high_pass_filter')
plt.plot(differiator(m[:]), label='differiator')
# plt.plot(db4_detail_coefficients(m), label='db4_detail_coefficients')
print("signal length: ", len(m))
plt.grid()
plt.legend()

cnt = 0
# assume that signal come from a sensor
i = 1000 # skip transient

MAX_TW = 5
while i< len(m): # skip transient
    if abs(m[i] - m[i-1]) > 5e2:
        print(f"[INFO] First TW Arrival at {i} us")
        # skip for 100us = 100 samples
        i += 100
        print(f"[INFO] Skip 100 samples, now at {i} us")
        cnt += 1
    else:
        i += 1
    if cnt >= MAX_TW:
        break

plt.show()

