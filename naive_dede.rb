def get_bit(k, i)
    bit = (k / (2**i)).floor.to_i - 2 * (k / (2**(i+1))).floor.to_i
    return bit
end

def func_m(n)
    two_n = (2**n)
    k_limit = (2**two_n)
    j_limit = (two_n - 1)

    z = 1

    k_prod = 0
    for k in (1..k_limit)
        j_prod = 1
        for j in (1..j_limit)
            i_prod = 1
            for i in (0..(j - 1))
                m_prod = 1
                m_limit = Math.log2(i)
                # if log(i) is equal to -inf skip
                # case of log(0)
                if m_limit != -Float::INFINITY
                    m_limit = m_limit.floor.to_i
                    for m in (0..m_limit)
                        bim = get_bit(i, m)
                        bjm = get_bit(j, m)
                        m_prod = m_prod * (1 - bim + bim * bjm)
                    end
                end
                bki = get_bit(k,i)
                bkj = get_bit(k,j)
                i_prod = i_prod * (1 - (m_prod * bki * bkj))
            end
            j_prod = j_prod *  i_prod
        end
        
        # if j_prod == 1 && k <= 2 ** 12 # if (k & (k - 1)) == 0
        #     # puts z.to_s + ":\t" + k.to_s + "\t" + j_prod.to_s + "\t" + k.to_s(2) 
        #     # print k.to_s + " "
        #     z += 1
        # end

        k_prod = k_prod + j_prod
    end

    return k_prod
end

iter = 6

# puts func_m(4)

iter.times do |i|
    t1 = Time.now
    res = func_m(i)
    t2 = Time.now

    puts "n#{i}: #{res} #{res.to_s(2)} | #{t2 - t1}"
end