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
    M4 = []
    _n = n - 4
    # Create elements from n-4 save them into M1
    #####################
    start_M = time.time()
    #####################
    M4 = create_M(_n)
    #####################
    end_M = time.time()
    print('M_time:\t\t' + str(end_M - start_M))    
    #####################
    start_alg = time.time()
    #####################
    r = np.zeros( ( len(M4), len(M4) ) )

    for i in range(0, len(M4)):
        for j in range(0, len(M4)):
            if eltwise_int(M4[i], M4[j]) is True:
                r[i][j] = 1

    re = np.matmul(r, r)

    # print(r)
    # print(re)

    for a in M4:
        print('a'+str(a) + ' ' + str(datetime.now()))
        for b in M4:
            print('b'+str(b) + ' ' + str(datetime.now()))
            for c in M4:
                print('c'+str(c) + ' ' + str(datetime.now()))
                for d in M4:
                    for e in M4:
                        for f in M4:
                            H = 0
                            h = 0
                            abd_index = find_index(a | b | d, M4)
                            ace_index = find_index(a | c | e, M4)
                            bcf_index = find_index(b | c | f, M4)
                            def_index = find_index(d | e | f, M4)
                            abc_index = find_index(a & b & c, M4)
                            ade_index = find_index(a & d & e, M4)
                            bdf_index = find_index(b & d & f, M4)
                            cef_index = find_index(c & e & f, M4) 
                            or_value = a | b | c | d | e | f
                            and_value = a & b & c & d & e & f                          
                            for u in range(0, len(M4)):
                                if eltwise_int(or_value, M4[u]):
                                    # u_index = find_index(u, M4)
                                    H = H + (re[abd_index][u] * \
                                            re[ace_index][u] * \
                                            re[bcf_index][u] * \
                                            re[def_index][u])
                            for v in range(0, len(M4)):
                                if eltwise_int(M4[v], and_value):
                                    # v_index = find_index(v, M4)
                                    h = h + (re[v][abc_index] * \
                                            re[v][ade_index] * \
                                            re[v][bdf_index] * \
                                            re[v][cef_index])
                            k += H * h
    #####################
    end_alg = time.time()
    print('alg_time:\t' + str(end_alg - start_alg))
    #####################
    # print('M1:')
    # print(M1)
    # print(arr_to_hex(M1))
    # print('M4:')
    # print(M4)
    # print(arr_to_bin(M4))
    #####################
    return k

def main():
    n = 8
    n_lookup = [2, 3, 6, 20, 168]

    res = algorithm(n)
    print("n" + str(n) +": " + str(res))
  
if __name__== "__main__":
    main()