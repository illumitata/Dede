import math
import numpy as np
import sys
import time

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

def algorithm(n):
    # Variables
    if n == 0:
        return 2
    k = 0
    M2 = []
    _n = n - 2
    # Create elements from n-2 save them into M1
    #####################
    start_M = time.time()
    #####################
    M2 = create_M(_n)
    #####################
    end_M = time.time()
    print('M_time:\t\t' + str(end_M - start_M))    
    #####################
    start_alg = time.time()
    #####################
    r = np.zeros( ( len(M2), len(M2) ) )

    for i in range(0, len(M2)):
        for j in range(0, len(M2)):
            if eltwise_int(M2[i], M2[j]) is True:
                r[i][j] = 1

    re = np.matmul(r, r)

    # print(r)
    # print(re)

    for i in range(0, len(M2)):
        for j in range(i, len(M2)): # why bother with 0's on the left
            d = re[i][j]
            # d += 1 # add one to count the index like distance
            k += d * d
    #####################
    end_alg = time.time()
    print('alg_time:\t' + str(end_alg - start_alg))
    #####################
    # print('M1:')
    # # print(M1)
    # print(arr_to_hex(M1))
    # print('M2:')
    # # print(M2)
    # print(arr_to_hex(M2))
    #####################
    return k

def main():
    n = 6
    n_lookup = [2, 3, 6, 20, 168]

    res = algorithm(n)
    print("n" + str(n) +": " + str(res))
  
if __name__== "__main__":
    main()