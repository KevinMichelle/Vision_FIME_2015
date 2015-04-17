from PIL import Image
import sys
import os.path
import utilities.files as files
import utilities.pix as pix
import utilities.neighbors as neighbors
import utilities.statistics as statistics

def filter_operator(image, filter_to_use):
	new_image = image.copy()
	xs, ys = image.size
	pixels = image.load()
	new_pixels = new_image.load()
	axis_limits = (ys, xs)
	for y in xrange(0, ys):
		for x in xrange(0, xs):
			pixel = (y, x)
			neighbor_pixels = neighbors.find_neighbors(pixels, pixel, None, axis_limits)
			values_neighbor = []
			for neighbor_pixel in neighbor_pixels:
				value_pixel = neighbor_pixel[1][0]
				values_neighbor.append(value_pixel)
			new_value = 0
			if filter_to_use == 'median':
				new_value = int(statistics.median(values_neighbor))
			new_pixels[x, y] = (new_value, new_value, new_value)
	return new_image