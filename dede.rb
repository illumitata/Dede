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

# def flip_bits(n, limit)
#     n_tmp = 1
#     new_n = n
#     while n_tmp < n
#         if (n_tmp & n) == 0
#             new_n += n_tmp 
#         else
#             new_n -= n_tmp
#         end
#         n_tmp = n_tmp << 1
#     end

#     while n_tmp < limit + 1
#         new_n += n_tmp
#         n_tmp = n_tmp << 1
#     end
        
#     return new_n
# end

def inner_loop(k, j_limit)
    # $terms += 1
    j_prod = 1
    # if k is in style of 2^n, where some n > 0
    # it always has a product of j_prod == 1
    # if (k & (k - 1)) != 0
    for j in (1..j_limit)
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

def func_m(n)
    # $terms = 0

    two_n = (2**n)
    k_limit = (2**two_n)
    j_limit = (two_n - 1)

    # Magic magic magic...
    # Just add 2 to the end result!
    # j-1 is always ending like:
    # k_limit = 'BBBBBBBBB'
    # j_max   = 'xxBBBBBBB', j_max = (2^n - 1)
    # Just cut the bullshit here :-D
    # Cause we never use the first to bits in
    # the formula. Same thing with:
    # i = j - 1 = (2^n - 1) - 1 = (2^n - 2(!!!))
    new_k_limit = set_all_true(k_limit >> 2)

    # puts "k_limit: #{k_limit}"
    # puts "new_k_limit: \n#{new_k_limit}"

    # z = 1
    # k_old = 0
    k_prod = 1 # 0

    limits = [
        [2, new_k_limit]
        # [2,128],
        # [256,384],
        # [512,640],
        # [1024,1664],
        # [2048,2176],
        # [4096,6272],
        # [8192,10368],
        # [16384,26752],
        # [32768,32768],
        # [65536,98304],
        # [131072,163840],
        # [262144,425984],
        # [524288,557056],
        # [1048576,1605632],
        # [2097152,2654208],
        # [4194304,6848512],
        # [8388608,8421376],
        # [16777216,25198592],
        # [33554432,41975808],
        # [67108864,109084672],
        # [134217728,142639104],
        # [268435456,411074560],
        # [536870912,679510016],
        # [1073741824, new_k_limit]
    ]

    limits.each do |lim|
        # for k in (lim[0]..lim[1])
        (lim[0]..lim[1]).step(2) do |k|
            # puts k.to_s + "\t\t" + Time.now.to_s if k % 10000000 == 0

            k_prod = k_prod + inner_loop(k, j_limit)
    
            # if j_prod == 1 # if (k & (k - 1)) == 0
            #     puts z.to_s + ":\t" + k.to_s + "\t" + j_prod.to_s + "\t" + k.to_s(2) 
            #     File.write('./z.txt', z.to_s + ' ', mode: 'a')
            #     if (k & (k - 1)) == 0
            #         ratio = (k - k_old) / 128 if k_old != 0
            #         File.write('./magic.txt', k_old.to_s + "\t" + k.to_s + "\t" + ratio.to_s + "\n", mode: 'a')
            #         File.write('./k.txt', '* ' + k.to_s + ' ', mode: 'a')
            #     else
            #         File.write('./k.txt', k.to_s + ' ', mode: 'a')
            #     end
            #     k_old = k
            #     z += 1
            # end
        end
    end

    return k_prod + 2
end

iter = 5

t1 = Time.now
res = func_m(4)
t2 = Time.now

puts "n: #{res} #{res.to_s(2)} | #{t2 - t1}"

# iter.times do |i|
#     t1 = Time.now
#     res = func_m(i)
#     t2 = Time.now

#     puts "n#{i}: #{res} #{res.to_s(2)} | #{t2 - t1} | #{$terms}"
# end