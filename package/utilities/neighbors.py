def neighbor_limits(parameters):
	dy_parameter, dx_parameter = parameters[0], parameters[1]
	lower_y = ((dy_parameter-1)/2)
	upper_y = ((dy_parameter+2)/2)
	lower_x = ((dx_parameter-1)/2)
	upper_x = ((dx_parameter+ 2)/2)
	limits = (lower_y, upper_y, lower_x, upper_x)
	return limits

def find_neighbors(nodes, initial_node, parameters, axis_limits):
	neighbors = []
	y, x = initial_node[0], initial_node[1]
	ys, xs = axis_limits[0], axis_limits[1]
	if parameters is not None:
		lower_y, upper_y, lower_x, upper_x = neighbor_limits(parameters)
	else: #neighborhood size -> 3 x 3
		lower_y, upper_y = 1, 2
		lower_x, upper_x = 1, 2
	for dy in xrange(y - lower_y, y + upper_y):
		if dy >= 0 and dy < ys:
			for dx in xrange(x - lower_x, x + upper_x):
				if dx >= 0 and dx < xs:
					if type(nodes) is tuple or type(nodes) is list:
						node_value = nodes[dx][dy]
					else: #nodes are pixels structure from PIL library
						node_value = nodes[dx, dy]
					node = (dy, dx)
					neighbors.append((node, node_value))
	return neighbors