from sympy.combinatorics import Permutation
from random import shuffle
import math

def waksman_route(positions):
    N = len(positions)
    
    #Positions- i is going to a[i]
    #Destinations- i is where a[i] is going
    #For bidirectional O(1) lookups
    destinations = [0]*N
    for i in range(N):
        destinations[positions[i]] = i
    
    
    if N == 2:
        return [[0]] if positions == [0, 1] else [[1]]
        
    
    #Recursive subpermutation assignments, 0 and 1 mean upper and lower
    sub_perm = [-1] * N
    
    for i in range(N):
        if sub_perm[i] == -1:
            curr = i
            
            # Set assignments by looping through a cycle
            while sub_perm[curr] == -1:
                # Assign current input to lower
                sub_perm[curr] = 0
                
                #Where current is going
                out_node = positions[curr]
                
                #Bitflip neighber of outnode
                out_neighbor = out_node ^ 1 
                
                #Where out_neighbor is coming from
                in_node = destinations[out_neighbor]
                
                # The bitflip neighbor goes to lower subpermutation
                sub_perm[in_node] = 1
                
                # bitflip neighbor goes to other subperm
                in_neighbor = in_node ^ 1
                curr = in_neighbor

    # 2. Extract sub-permutations and set outer stage switches
    P_up = [0] * (N // 2)
    P_down = [0] * (N // 2)
    
    in_swaps = []
    out_swaps = []
    
    # First stage (input switches)
    for k in range(N // 2):
        # If input 2k goes to upper, switch k is unset 
        # If input 2k goes to lower, switch k is set (swap)
        if sub_perm[2 * k] == 0:
            in_swaps.append(0)
        else:
            in_swaps.append(1)
            
    for i in range(N):
        if sub_perm[i] == 0:
            P_up[i // 2] = positions[i] // 2
        else:
            P_down[i // 2] = positions[i] // 2
            
    # Same dimension, going back up
    for k in range(N // 2):
        in_node = destinations[2 * k]

        if sub_perm[in_node] == 0:
            out_swaps.append(0)
        else:
            out_swaps.append(1)

    up_settings = waksman_route(P_up)
    down_settings = waksman_route(P_down)

    stages = [in_swaps]
    
    # The inner stages consist of the upper and lower swaps stacked
    for s in range(len(up_settings)):
        stages.append(up_settings[s] + down_settings[s])
        
    stages.append(out_swaps)

    return stages

def apply_network(wires, stages):
    N = len(wires)
    if N == 2:
        w = list(wires)
        if stages[0][0]:
            w[0], w[1] = w[1], w[0]
        return w

    half = N // 2
    w = list(wires)

    # Swap first stages
    for k, swap in enumerate(stages[0]):
        if swap:
            w[2*k], w[2*k+1] = w[2*k+1], w[2*k]

    # Split list
    upper = [w[2*i] for i in range(half)]
    lower = [w[2*i+1] for i in range(half)]

    # Split remaining stages and apply swaps recursively
    inner = stages[1:-1]
    #Split based on parity, since least significant bit first
    upper = apply_network(upper, [s[:half//2] for s in inner])
    lower = apply_network(lower, [s[half//2:] for s in inner])

    # Recombine 
    for i in range(half):
        w[2*i]   = upper[i]
        w[2*i+1] = lower[i]

    #Swap last stages
    for k, sw in enumerate(stages[-1]):
        if sw:
            w[2*k], w[2*k+1] = w[2*k+1], w[2*k]

    return w

target = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]

shuffle(target)
print(target)
swaps = waksman_route(target)
    
print("SWAPS")
for k, stage in enumerate(swaps):
    print(f"Stage {k}: {stage}")

print(apply_network(target, swaps))