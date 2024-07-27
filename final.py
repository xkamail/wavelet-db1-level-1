import numpy as np
from matplotlib import pyplot as plt
import math 

def get_sign(value):
    if value > 0:
        return 1
    elif value < 0:
        return -1
    else:
        return 0

def differiator(x,scale=1):
    d = np.zeros(len(x))
    for n in range(len(x)):
        d[n] = scale*(x[n] - x[n-1])
    return d

def peak_finder(x = [], color = 'red',max_tw = 5):
    results = []
    i = 50 # skip transient 50us
    while i < len(x):
        cnt = len(results)
        if abs(x[i] - x[i-1]) > 3e2:
            print(f"TW detected T{cnt}={i} us slope", int(math.copysign(1, x[i]-x[i-1])))
            plt.plot(i, 0, 'o',color=color, label=f'T{cnt}={i} us')
            i += 5 # skip 5us
            results.append(i)
        else:
            i += 1
        if len(results) >= max_tw:
            break
    return results

m = np.genfromtxt('m.csv', delimiter=',')
n = np.genfromtxt('n.csv', delimiter=',')

m_diff = differiator(m)
n_diff = differiator(n)

plt.plot(m_diff, label='bus-m-diff')
plt.plot(n_diff, label='bus-n-diff')
plt.grid()

print("M Bus")
m_tw = peak_finder(m_diff, 'blue',5)
print("=====================================")
print("N Bus")
n_tw = peak_finder(n_diff, 'orange',5)

# Normal calculator
# 1/2 (100km + (t1-t2) * 0.3km/us)

if len(m_tw) > 1 and len(n_tw) > 1:
    c1 = 0.5 * (100 + (m_tw[0] - n_tw[0]) * 0.289942)
    print(f"Distance calculation: {c1} km")
    

plt.legend()
plt.show()