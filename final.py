import numpy as np
from matplotlib import pyplot as plt

# config
PREFIX = '80_20'
# PREFIX = '70_30'
# PREFIX = '40_60'
# PREFIX = '50_50'
# PREFIX = '90_10'
# PREFIX = '95_5'
# config

# scaling coefficients
h = [
    (1+np.sqrt(3))/(4*np.sqrt(2)),
    (3+np.sqrt(3))/(4*np.sqrt(2)),
    (3-np.sqrt(3))/(4*np.sqrt(2)),
    (1-np.sqrt(3))/(4*np.sqrt(2)),
    (1+np.sqrt(3))/(4*np.sqrt(2)),
    (3+np.sqrt(3))/(4*np.sqrt(2)),
    (3-np.sqrt(3))/(4*np.sqrt(2)),
    (1-np.sqrt(3))/(4*np.sqrt(2)),
]
# wavelet coefficients
g=[h[3], -h[2], h[1], -h[0], h[7], -h[6], h[5], -h[4]]

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
        for k in range(8):
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

def peak_finder(x = [], color = 'red',dt=0):
    lookahead = 8
    mx = -np.inf
    max_peaks = []
    foundTW = False
    i=0
    std = np.std(x[2000:4000]) /2
    print(std)
    lastest_comp = 0
    while i < len(x)-lookahead:
        i += 1
        y = x[i]
        # detect first spike of TW 
        if (x[i]-x[i+lookahead]) > 500:
            foundTW = True
            mx = y
            mxpos = i
        if not foundTW:
            continue  
        # limit size of buffers
        if len(max_peaks) > 5:
            break
        if y > mx:
            mx = y
            mxpos = i
        # find max
        if y < mx and mx != np.inf:
            # index of latest max is diff by 4 then skip
            comp = np.abs(x[i:i+lookahead]).max()
            if comp < 0:
                continue
            if abs(lastest_comp-comp) < 1:
                continue
            if comp < mx:
                
                print(f"TW detected T{len(max_peaks)}={mxpos} value=", mx, comp,flush=True)
                max_peaks.append(mxpos)
                mx = -np.inf
                i += lookahead//2
                if i+lookahead >= len(x):
                    break
            lastest_comp = comp
    # max_peaks.pop(0)
    return max_peaks

m = np.genfromtxt(PREFIX+'/m.csv', delimiter=',')
n = np.genfromtxt(PREFIX+'/n.csv', delimiter=',')

# m_diff = differiator(m)
# n_diff = differiator(n)
m_diff = db4_detail_coefficients(m)
n_diff = db4_detail_coefficients(n)


plt.plot(m_diff, label='bus-m-process')
plt.plot(n_diff, label='bus-n-process')
plt.grid()

print("M Bus")
m_tw = peak_finder(m_diff)

print("=====================================")
print("N Bus")
n_tw = peak_finder(n_diff)
print("=====================================")
if len(m_tw) == 0 or len(n_tw) == 0:
    print("No TW detected")
    plt.show()
    exit()
print("M TW: ", m_tw)
print("N TW: ", n_tw)
for i in m_tw:
    plt.plot(i, 0, 'o',color='blue', label=f'M TW={i} us')
for i in n_tw:
    plt.plot(i, 0, 'o',color='red', label=f'N TW={i} us')

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