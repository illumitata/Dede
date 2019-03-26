def get_bit(k, i)
    return 1 if ((k >> i) & 1) == 1
    return 0
end

# Aprox dla większych serii, bez użycia float
def log_aprox(n)
    if n == 0 || n == 1
        return 0
    elsif n == 2
        return 1
    else
        tmp = 2 * 2
        x = 1

        loop do
            break if tmp > n
            tmp = tmp * 2
            x += 1
        end
        
        return x
    end
end

# Czy jest tylko jeden bit --> potęga dwójki
def only_one(n)
    return (n & (n - 1)) == 0
end

# Czy jest każy jeden bit --> set od pierwszego momentu do końca
# 0 gdy nie wszystkie, inaczej zwróć ich liczbę
def all_set(n)
    # jeśli tylko jeden to oczywiste
    return 0 if only_one(n)

    count = 0
    while n != 0
        bit = n & 1
        return 0 if bit == 0
        count += bit
        n = n >> 1
    end
        
    return count
end

def set_all_true(n)        
    n_tmp = 1
    new_n = n
    while n_tmp < n
        new_n += n_tmp 
        n_tmp = n_tmp << 1
    end
        
    return new_n
end

def inner_loop(k)
    j_prod = 1
    for j in (1..$j_limit)
        i_prod = 1
        for i in (0..(j - 1))
            bki = get_bit(k,i)
            bkj = get_bit(k,j)
            # Pierwsza optymalizacja, jeśli bki * bkj == 1
            # pomiń obieg pętli.
            if bki * bkj == 1
                m_prod = 1
                m_limit = log_aprox(i)
                # puts m_limit
                # Wykluczmy przypadki i = 0 i m = 0
                # Tylko o takich wiem, to jest dość dziwne
                # mniej inicjacji pustych pętli???
                if (i != 0 || m_limit != 0)
                    for m in (0..m_limit)
                        bim = get_bit(i, m)
                        bjm = get_bit(j, m)
                        # Możemy zauważyć, że jeżeli
                        # bim == 1 oraz bjm == 0
                        # m_prod staje się 0, co można już zwrócić
                        # zdecydowanie wcześniej
                        if bim == 1 && bjm == 0
                            m_prod = 0
                            break
                        end
                    end
                end
                ####################################
                i_prod = i_prod * (1 - (m_prod * bki * bkj))
                # Po co liczyć jeżeli już 0?
                break if i_prod == 0
            end
        end
        j_prod = j_prod *  i_prod
        # Po co liczyć jeżeli już 0?
        break if j_prod == 0
    end

    return j_prod
end

def splitter(left, right)
    # puts "#{left} #{right}"
    if right - left < 2
        a = 0
        b = 0
        a = inner_loop(left) if left % 2 == 0
        b = inner_loop(right) if right % 2 == 0
        return a + b
    else
        split_m = ((right + left) / 2).floor.to_i
        res = splitter(left, split_m) + splitter(split_m + 1, right)
        return res
    end
end

def func_m(n)
    two_n = (2**n)
    k_limit = (2**two_n)
    $j_limit = (two_n - 1)
    new_k_limit = set_all_true(k_limit >> 2)
    limits = [1, new_k_limit]
    split_m = ((limits[1] + limits[0]) / 2).floor.to_i
    return splitter(limits[0], split_m) + splitter(split_m + 1, limits[1]) + 3
end

t1 = Time.now
res = func_m(4)
t2 = Time.now

puts "n: #{res} #{res.to_s(2)} | #{t2 - t1}"