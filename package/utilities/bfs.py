import utilities.neighbors as neighbors

def four_way(pixel, neighbor_pixels):
	y, x = pixel
	neighbors_four_way = list()
	for neighbor in neighbor_pixels:
		dy, dx = neighbor[0]
		if ((dy == y - 1) and (dx == x)) or ((dy == y) and (dx == x - 1)) or ((dy == y) and (dx == x + 1)) or ((dy == y + 1) and (dx == x)):
			neighbors_four_way.append((dy, dx))
	return neighbors_four_way

def bfs(image, queue_neighbors, oldcolor, newcolor, visited): #checar nombre
	pixels = image.load()
	xs, ys = image.size
	y, x = queue_neighbors.pop(0)
	pixel_value = pixels[x, y]
	if oldcolor == newcolor:
		return
	if pixel_value != oldcolor:
		return
	pixels[x, y] = newcolor
	pixel, parameters, axis_limits = (y, x), None, (ys, xs)
	neighbor_pixels = neighbors.find_neighbors(pixels, pixel, parameters, axis_limits)
	neighbors_four_way = four_way(pixel, neighbor_pixels)
	for neighbor in neighbors_four_way:
		if neighbor not in visited:
			dy, dx = neighbor
			neighbor_value = pixels[dx, dy]
			if neighbor_value == oldcolor:
				queue_neighbors.append(neighbor)
				visited[neighbor] = 1
	return None
