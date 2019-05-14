import math
import numpy as np
import sys
import time
from datetime import datetime

def concat_int(x, y, offset):
    '''
    Concatenate x with y with given offset on x.
    Func:
        return (x << offset) + y    
    '''
    return (x << offset) + y

def eltwise_int(x, y):
    '''
    Check if x <= y with the definition:
        x = (x1, ... , xn)
        y = (y1, ... , yn)
        x <= y if and only if xi <= xy for 1 <= i <= n
    '''
    if (x | y) == y:
        return True
    else:               # remove it? Just return false
        return False

def create_M(n):
    '''
    Create M with n index - set of all "elements".
    Where "element" stands for boolean monotone function.
    '''
    _M = [0, 1] # standard set of basic boolean functions M0
    _M_tmp = [] # temporary array for M
    for _n in range(0, n):
        for i in range(0, len(_M)):
            for j in range(i, len(_M)):
                if eltwise_int(_M[i], _M[j]) is True:
                    # print(bin(_M[i]) + ' ' + bin(_M[j]))
                    # print(str(concat_int(_M[i], _M[j], 2 ** _n)) + ' ' + str(_n))
                    _M_tmp += [concat_int(_M[i], _M[j], 2 ** _n)] # add to temporary
        _M = _M_tmp  # add temporary to _M
        _M_tmp = []  # clear _M_tmp
    return _M

def arr_to_hex(arr):
    _arr = []
    for _m in arr:
        _arr.append(hex(_m))
    return _arr

def arr_to_bin(arr):
    _arr = []
    for _m in arr:
        _arr.append(bin(_m))
    return _arr

def find_index(m, M):
    for i in range(0, len(M)):
        if m == M[i]:
            return i
    return None

def algorithm(n):
    # Variables
    if n == 0:
        return 2
    k = 0
    M3 = []
    _n = n - 3
    # Create elements from n-3 save them into M1
    #####################
    start_M = time.time()
    #####################
    M3 = create_M(_n)
    #####################
    end_M = time.time()
    print('M_time:\t\t' + str(end_M - start_M))    
    #####################
    start_alg = time.time()
    #####################
    r = np.zeros( ( len(M3), len(M3) ) )

    for i in range(0, len(M3)):
        for j in range(0, len(M3)):
            if eltwise_int(M3[i], M3[j]) is True:
                r[i][j] = 1

    re = np.matmul(r, r)

    # print(r)
    # print(re)

    for a in M3:
        for b in M3:
            for c in M3:
                H = 0
                h = 0
                a_index = find_index(a, M3)
                b_index = find_index(b, M3)
                c_index = find_index(c, M3)
                ab_index = find_index(a & b, M3)
                bc_index = find_index(b & c, M3)
                ac_index = find_index(a & c, M3)
                or_value = a | b | c
                and_value = a & b & c                          
                for u in range(0, len(M3)):
                    if eltwise_int(or_value, M3[u]):
                        H = H + (re[a_index][u] * \
                                re[b_index][u] * \
                                re[c_index][u])
                for v in range(0, len(M3)):
                    if eltwise_int(M3[v], and_value):
                        h = h + (re[v][ab_index] * \
                                re[v][bc_index] * \
                                re[v][ac_index])
                k += H * h
    #####################
    end_alg = time.time()
    print('alg_time:\t' + str(end_alg - start_alg))
    #####################
    # print('M1:')
    # print(M1)
    # print(arr_to_hex(M1))
    # print('M3:')
    # print(M3)
    # print(arr_to_bin(M3))
    #####################
    return k

def main():
    n = 4
    n_lookup = [2, 3, 6, 20, 168]

    res = algorithm(n)
    print("n" + str(n) +": " + str(res))
  
if __name__== "__main__":
    main()