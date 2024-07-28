import numpy as np
from matplotlib import pyplot as plt

# config
THRESHOLD = 15   
PREFIX = '90_10'
# config

# scaling coefficients
h = [
    (1+np.sqrt(3))/(4*np.sqrt(2)),
    (3+np.sqrt(3))/(4*np.sqrt(2)),
    (3-np.sqrt(3))/(4*np.sqrt(2)),
    (1-np.sqrt(3))/(4*np.sqrt(2)),
]
# wavelet coefficients
g=[h[3], -h[2], h[1], -h[0]]

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

def peak_finder(x = [], color = 'red',max_tw = 5):
    results = []
    i = 10000 # skip transient 0.5k samples
    width = 6
    while i <  len(x)-width:
        cnt = len(results)
        v = abs(x[i] - x[i-width]) # width 4 samples to prevent slower rate
        if v > THRESHOLD:
            print(f"TW detected T{cnt}={i} value=", v, v//width)
            plt.plot(i, 0, 'o',color=color, label=f'T{cnt}={i} us')
            results.append(i)
            i += width+10 # skip next width
        else:
            i += 1
        if len(results) >= max_tw:
            break
    return results

m = np.genfromtxt(PREFIX+'/m.csv', delimiter=',')
n = np.genfromtxt(PREFIX+'/n.csv', delimiter=',')

T = 2e-6

# m_diff = differiator(m)
# n_diff = differiator(n)
m_diff = db4_detail_coefficients(m)
n_diff = db4_detail_coefficients(n)


plt.plot(m_diff, label='bus-m-process')
plt.plot(n_diff, label='bus-n-process')
plt.grid()

print("M Bus")
m_tw = peak_finder(m_diff, 'blue',5)
print("=====================================")
print("N Bus")
n_tw = peak_finder(n_diff, 'orange',5)
print("=====================================")

if len(m_tw) == 0 or len(n_tw) == 0:
    print("No TW detected")
    plt.show()
    exit()
# Normal calculator
# 1/2 (100km + (t1-t2) * 0.3km/us)

if len(m_tw) > 1 and len(n_tw) > 1:
    c1 = 0.5 * (100 + (m_tw[0] - n_tw[0]) * 0.289942)
    print(f"Distance calculation: {c1} km")
    

# New Calculation
dm = m_tw[1] - m_tw[0]
dn = n_tw[1] - n_tw[0]
l = 100 # km
d_m = l/((
    dn/dm
)+1)

print(f"New Distance Calculation from Bus M is {d_m} km")

d_n =  l/((
    dm/dn
)+1) 

print(f"New Distance Calculation from Bus N is {d_n} km")

plt.xlabel('Time (us)')

plt.legend()
plt.show(
)