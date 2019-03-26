import math
import numpy as np

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

def create_g_lookup(limit):
    if limit == 0:
        arr = [0, 1]
    else:
        arr = [0] # add zero here, because below trick ommits it
        arr_tmp = []
        g_parts = []
        # first split and than rest of them
        g_parts += concat('0', limit - 1)
        g_parts += concat('1', limit - 1)
        # tricky thing
        print(g_parts)
        i = 0
        for g in g_parts:
            _g = int(g, 2)
            if _g == 0 or _g % 2 != 0:
                for j in range(i, len(g_parts)):
                    _g_element = g + g_parts[j]
                    g_element = int(_g_element, 2)
                    if g_element % 2 != 0: # g_element % 2 == 1
                        arr_tmp.append(_g_element)
                        arr.append(g_element)
            i += 1
        print(arr_tmp)
        print(arr)
    return arr

def algorithm2(n, n_prev):
    ''' Input M(n-2) '''
    print(n_prev)
    g_lookup = create_g_lookup((n - 2))
    # Init of R
    r = np.random.randint(0, 1, size = (n_prev, n_prev))# (n_prev, n_prev))
    # Replace with r[u, v]:
    # 1, when u <= v
    # 0, otherwise
    for v in range(len(r)):
        for u in range(len(r[v])):
            if u <= v:
                r[v][u] = 1
            else:
                r[v][u] = 0
    # Compute Re = R x R
    re = np.matmul(r, r)
    print(re)
    # Calculate the sum over Re
    res = 0
    i = 0
    for v in g_lookup:
        for u in g_lookup:
            if u <= v:
                _v = v
                _u = u
                if v >= len(re[0]):
                    _v = n_prev - 1
                if u >= len(re[0]):
                    _u = n_prev - 1
                print(str(re[_v][_u]) + " v:" + str(v) + " u:" + str(u)) 
                res += re[_v][_u] * re[_v][_u]
    return res

def main():
    n = 4
    n_lookup = [2, 3, 6, 20, 168]

    res2 = algorithm2(n, n_lookup[n - 2])
    print("alg2: " + str(res2))
  
if __name__== "__main__":
    main()