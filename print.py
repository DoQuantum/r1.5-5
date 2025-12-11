import math

from list_to_cycles import list_to_cycles
from draw_edges import draw_edges

def print_r(arr:list[int]) -> None:
    l = int(math.sqrt(len(arr)))
    print(arr)
    for y in range(l):
        for x in range(l):
            print(f'{arr[x+l*y]:04b}', end=' ')
        print('')
    print('')

def print_e(red:list[int], green:list[int], blue:list[int]):
	cycles = list_to_cycles(red, green, blue)
	draw_edges(cycles) # draw nice png

	ansi = {'red':"\x1B[41m",'green':"\x1B[42m",'blue':"\x1B[44m",0:"\x1B[0m"}

	for cycle in cycles:
		for (i, j, color) in cycle:
			print(f"{i:02}{ansi[color]} {ansi[0]}", end='')
		print()