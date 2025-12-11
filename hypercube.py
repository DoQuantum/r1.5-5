from sympy.combinatorics import Permutation
from random import shuffle
import math

from print import *

def get_kth_bit(n, k):
	return n >> k & 1
	#return int(n/math.pow(2, k))%2

def generate_swaps(red, green, blue):
	"""
	finds a perfect matching

	:param red: edges 
	"""
	print_e(red, green, blue)

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
		while(not(next in found)):
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

def route(initial_state:list[int]):
	"""
	generate a list of pairwise swaps optimally

	:param target: 1 × 2^2^n list of locations
	"""

	# get shape of grid
	# assume rows >= cols
	# both of form 2^k or 2^k & 2^(k+1)
	l = len(initial_state)
	l_len = math.log2(l) / 2
	if l_len % 1 == 0.5:
		rows = 2 ** int(math.ceil(l_len))
		cols = 2 ** int(math.floor(l_len))
	else:
		rows = cols = 2 ** int(l_len)

	# dimension of hypercube
	dim = int(math.log2(l))

	# state of the actual atom array
	array_state = initial_state

	# target permutation
	sigma = Permutation(initial_state)

	# color template with no swaps
	blank = [-1] * l

	#Add green/blue edges
	#edges are tuples of 2 points

	# over every bit in the destination location bitstring (backwards)
	for bit in reversed(range(dim)):
		sigma_arr = sigma.array_form
		#print(sigma_arr)

		green = blank.copy()
		red = blank.copy()
		blue = blank.copy()

		# for each atom in the array
		for i in range(l):

			#edges are undirected, so only create from 0 at kth bit
			# green edges: location bits differ
			if get_kth_bit(i, bit) == 0: # get_kth_bit(i+2**bit,bit)
				green[i] = i + 2**bit # +add vs ^xor is the same because i[bit]==0
				green[i + 2**bit] = i

			# red/blue edges: destination bit differs
			if get_kth_bit(sigma_arr[i], bit) == 0:
				#O(n) search, need to optimize
				match = sigma_arr.index(sigma_arr[i] + 2**bit)

				# red: different destination bit, same at current bit
				# blue: different destination and current bit
				if(get_kth_bit(i, bit) == get_kth_bit(match, bit)):
					red[i] = match
					red[match] = i
				else:
					blue[i] = match
					blue[match] = i
		# swaps in current step in array and cyclic form
		bit_swaps = generate_swaps(red, green, blue)
		sigma1 = Permutation(bit_swaps)
		print(sigma1)
		#perform sigma1 on the "physical array" and update sigma for the "recursive step"
		sigma = sigma1 * sigma * sigma1
		array_state = sigma1(array_state)
		print(array_state)
	
	#Pairs on the wrong side of the cut are swapped
	#Reverse order of the matching step to mimic recursive structure
	
	for k in range(dim):
		for i in range(l):
			if(get_kth_bit(i, k) == 0 and get_kth_bit(array_state[i], k) == 1):
				temp = array_state[i]
				array_state[i] = array_state[i + 2**k]
				array_state[i + 2**k] = temp
	#should be sorted array
	print_r(array_state)




#2D array is represented as a 1D array where each index 
#is the concatened binary string of the row and column indicies
start = list(range(16))
shuffle(start)
print(start)
route(start)