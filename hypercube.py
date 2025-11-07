from sympy.combinatorics import Permutation
import math

def print_r(arr:list[int]) -> None:
    l = int(math.sqrt(len(arr)))
    print(arr)
    for y in range(l):
        for x in range(l):
            print(f'{arr[x+l*y]:04b}', end=' ')
        print('')
    print('')

def get_kth_bit(n, k):
    return int(n/math.pow(2, k))%2

def generate_swaps(red, green, blue):
    #finds a perfect matching
    found = set()
    perfect_matching = set()
    sigma1 = []
    for i in range(len(red)):
        sigma1.append(i)
    
    for i in range(len(red)):
        if(i in found or red[i] == -1):
            continue
        matching1 = set()
        matching2 = set()
        parity = True
        last_green = False
        found.add(i)
        next = red[i]
        #iterate through cycle containing current red edge
        while(True):
            if(next in found):
                break
            if(last_green):
                if(blue[next] == -1):
                    found.add(next)
                    next = red[next]
                    parity = not parity
                    last_green = False
                else:
                    next = blue[next]
                    last_green = False
            else:
                if(parity):
                    matching1.add((next, green[next]))
                else:
                    matching2.add((next, green[next]))
                next = green[next]
                last_green = True
            
        
        if(len(matching1)>len(matching2) and len(matching2) != 0):
            perfect_matching.update(matching2)
        else:
            perfect_matching.update(matching1)
    
    for i in perfect_matching:
        sigma1[i[0]] = i[1]
        sigma1[i[1]] = i[0]
    #return green edges in perfect matching
    return sigma1

def route(target, rows, cols):
    final = target
    sigma = Permutation(target)
    arr_n = target
    dim = int(math.log2(rows*cols))
    
    #Add green/blue edges
    #edges are tuples of 2 points
    for k in range(dim-1, -1 ,-1):
        arr_n = sigma.array_form
        green = [-1]*rows*cols
        red = [-1]*rows*cols
        blue = [-1]*rows*cols
        #print(arr_n)
        for i in range(rows*cols):
            #edges are undirected, so only create from 0 at kth bit
            if(get_kth_bit(i, k) == 0):
                green[i] = i+int(math.pow(2, k))
                green[i+int(math.pow(2, k))] = i
            if(get_kth_bit(arr_n[i], k) == 0):
                #O(n) search, can probably optimize
                match = arr_n.index(arr_n[i]+ int(math.pow(2, k)))
                if(get_kth_bit(i, k) == get_kth_bit(match, k)):
                    red[i] = match
                    red[match] = i
                else:
                    blue[i] = match
                    blue[match] = i
        
        k_swaps = generate_swaps(red, green, blue)
        sigma1 = Permutation(k_swaps)
        print(sigma1)
        sigma = sigma1 * sigma * sigma1
        final = sigma1(final)
        

    arr_n = final
    for k in range(dim):
        for i in range(rows*cols):
            if(get_kth_bit(i, k) == 0 and get_kth_bit(i, k) != get_kth_bit(arr_n[i], k)):
                temp = arr_n[i]
                arr_n[i] = arr_n[i + int(math.pow(2, k))]
                arr_n[i + int(math.pow(2, k))] = temp
    print_r(arr_n)





start = [11, 0, 6, 10, 5, 15, 2, 3, 13, 12, 7, 8, 9, 1, 4, 14]
route(start, 4, 4)
