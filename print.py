import math

def print_r(arr:list[int]) -> None:
    l = int(math.sqrt(len(arr)))
    print(arr)
    for y in range(l):
        for x in range(l):
            print(f'{arr[x+l*y]:04b}', end=' ')
        print('')
    print('')
