from sympy.combinatorics import Permutation
import math

from print import print_r

def get_kth_bit(n, k):
	return n >> k & 1;
	#return int(n/math.pow(2, k))%2

def generate_swaps(red, green, blue):
	"""
	finds a perfect matching

	:param red: edges 
	"""

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

def route(target:list[int]):
	"""
	generate a list of pairwise swaps optimally

	:param target: 1 × 2^2^n list of locations
	"""

	# get shape of grid
	# assume rows >= cols
	# both of form 2^k or 2^k & 2^(k+1)
	l = len(target)
	l_len = math.log2(l) / 2
	if l_len % 1 == 0.5:
		rows = 2 ** int(math.ceil(l_len))
		cols = 2 ** int(math.floor(l_len))
	else:
		rows = cols = 2 ** int(l_len)

	# dimension of hypercube
	dim = int(math.log2(l))

	# what the final permutation composition should look like
	final = target

	# permutation representation of final state
	sigma = Permutation(final)

	# color template with no swaps
	blank = [-1] * l

	#Add green/blue edges
	#edges are tuples of 2 points

	# over every bit in the destination location bitstring (backwards)
	for bit in reversed(range(dim)):
		arr_n = sigma.array_form
		#print(arr_n)

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

			# red/blue edges: current destination bit differs
			if get_kth_bit(arr_n[i], bit) == 0:
				#O(n) search, can probably optimize
				match = arr_n.index(arr_n[i] + 2**bit)

				# red: different destination bit, same at current bit
				# blue: different destination and current bit
				if(get_kth_bit(i, bit) == get_kth_bit(match, bit)):
					red[i] = match
					red[match] = i
				else:
					blue[i] = match
					blue[match] = i
		
		bit_swaps = generate_swaps(red, green, blue)
		sigma1 = Permutation(bit_swaps)
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
route(start)
