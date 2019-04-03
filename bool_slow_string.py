import math
import numpy as np
import sys
import time

def concat(_M, limit):
    if limit == 0:
        return [_M]
    elif limit == 1:
        arr = []
        arr += [_M + '0']
        arr += [_M + '1']
        return arr
    else:
        left = concat(_M + '0', limit - 1)
        right = concat(_M + '1', limit - 1)
        return left + right

def check_eltwise(m1, m2):
    if len(m1) != len(m2):
        print('Error while checking eltwise!')
        sys.exit()        
    for i in range(0, len(m1)):
        if m1[i] > m2[i]: # int(m1[i]) > int(m2[i]): 
            return False
    return True

def check_monotone(m):
    if len(m) < 2:
        return True
        # print('Error while checking monotone!')
        # sys.exit()
    elif len(m) == 2:
        if m[0] > m[1]: # int(m[0]) > int(m[1]):
            return False
        return True
    else:
        f_half, s_half = m[:len(m)//2], m[len(m)//2:]
        if check_eltwise(f_half, s_half) == False:
            return False
        left = check_monotone(f_half)
        right = check_monotone(s_half)
        return (left and right)

def create_M(n):
    M = []
    n = 2 ** n
    _M = []
    _M += concat('0', n - 1)
    _M += concat('1', n - 1)
    # print(len(M))
    # Check monotone functions
    for _m in _M:
        if check_monotone(_m) is True:
            M.append(_m)
    return M

def arr_to_hex(arr):
    _arr = []
    for _m in arr:
        _arr.append(hex(int(_m, 2)))
    return _arr

def algorithm(n):
    if n == 0:
        return 2
    # Variables
    k = 0
    M2 = []
    # Create elements from n-1 save them into M1
    #####################
    start_M = time.time()
    #####################
    M1 = create_M(n - 1)
    #####################
    end_M = time.time()
    print('M_time:\t\t' + str(end_M - start_M))    
    #####################
    start_alg = time.time()
    #####################
    for i in M1:
        for j in M1:
            if check_eltwise(i, j) == True:
                k += 1
                M2.append(i + j) # concatenate them
    #####################
    end_alg = time.time()
    print('alg_time:\t' + str(end_alg - start_alg))
    #####################
    # print('M1:')
    # print(M1)
    # print(arr_to_hex(M1))
    # print('M2:')
    # print(M2)
    # print(arr_to_hex(M2))
    #####################
    return k

def main():
    n = 5
    n_lookup = [2, 3, 6, 20, 168]

    res = algorithm(n)
    print("n" + str(n) +": " + str(res))
  
if __name__== "__main__":
    main()