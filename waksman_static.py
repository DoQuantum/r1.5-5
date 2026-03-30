# Generator for Waksman networks

import numpy as np



def permutation(in_order:list[int], out_order:list[int]) -> np.ndarray:
	r'''
	turn a demonstrated permutation into the corresponding matrix form

	:param in_order: before the permutation
	:param out_order: after the permutation
	:return: permutation in matrix representation
	'''

	# size of permuted set
	l = len(in_order)
	assert l == len(out_order)

	# permutation matrix
	m = np.zeros((l, l), dtype=int)
	m[(in_order, out_order)] = 1

	return m


def waksman_fixed(n:int) -> list[np.ndarray]:
	r'''
	return the fixed steps of the waksman algorithm.
	these steps lie between each situation-dependent layer of the permutation network.

	:param n: number of points in the network
	:return: list of permutation matrices
	'''

	# bits to iterate over
	bits = int(np.log2(n))
	assert n == 1 << bits

	ans = []
	eye = np.eye(n, dtype=int)
	idx = list(range(n))

	# create the first half of the network
	for round_number in range(bits - 1):
		ans.append(
			# rearrange by differing bits
			eye[sorted(
				idx,
				key = lambda v: (v & (1 << round_number)) >> round_number,
			)]
		)

	# the second half of the network is the inverse of the first half
	# permutation matrices are unitary, so the inverse is the transpose
	for ansT in ans[-1::-1]:
		ans.append(ansT.T)

	return ans



if __name__ == '__main__':
	# example of n=8 from doi/10.1145/321439.321449
	n = 8
	a = [
		[0, 1, 2, 3, 4, 5, 6, 7],
		[0, 2, 4, 6, 1, 3, 5, 7],
		[0, 4, 2, 6, 1, 5, 3, 7],
		[0, 2, 4, 6, 1, 3, 5, 7],
	]
	p = [
		permutation(a[i], a[i + 1])
		for i in range(len(a) - 1)
	]
	m = waksman_fixed(n)

	for mi, pi in zip(p, m):
		assert np.all(mi == pi)

	print(f'check passed @ n={n}')