def list_to_cycles(red:list[int], green:list[int], blue:list[int]):
	"""
	turn zarif's rgb edge lists into a cycle
	
	:param red: arr[x]=y, arr[y]=x, -1 indicates no connection
	:param green: see red
	:param blue: see red
	:return: list of cycles
	"""
	
	# if the graph is fully connected, the column sums in our representation will be (-2 .. n-2). implementation specific?
	
	x:int = 0
	cycle:list[tuple[int,color:str]] = []
	cycles:list[cycle] = []
	visited = [False] * len(red)
	
	while not all(visited):
		visited[x] = True
		if red[x] != -1 and not visited[red[x]]:
			cycle.append((x, red[x], 'red'))
			x = red[x]
		elif green[x] != -1 and not visited[green[x]]:
			cycle.append((x, green[x], 'green'))
			x = green[x]
		elif blue[x] != -1 and not visited[blue[x]]:
			cycle.append((x, blue[x], 'blue'))
			x = blue[x]
		else:
			if red[x] != -1:
				cycle.append((x, cycle[0][0], 'red'))
			elif green[x] != -1:
				cycle.append((x, cycle[0][0], 'green'))
			elif blue[x] != -1:
				cycle.append((x, cycle[0][0], 'blue'))
			cycles.append(cycle)
			cycle = []
			x = next((i for i,x in enumerate(visited) if not x), None)
			if x is None: break
	
	del x, cycle, visited
	return cycles