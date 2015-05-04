from PIL import Image
import sys
import os.path
import random
import math
import utilities.files as files
import utilities.filters as filters
import utilities.statistics as statistics
import utilities.pix as pix
import utilities.masks as masks

def binarized_image(image):
	xs, ys = image.size
	pixels = image.load()
	new_image = image.copy()
	new_pixels = new_image.load()
	frec_col = pix.frec_colors(image)
	total = xs * ys
	threshold = 0.005 * total
	min_value, max_value = 1000000, -1000000
	#print threshold
	for col_value in frec_col:
		if frec_col[col_value] > threshold:
			value = col_value[0] 
			if value < min_value:
				min_value = value
			if value > max_value:
				max_value = value
	range_value = max_value - min_value
	#print min_value, max_value, range_value
	#for e in frec_col:
	#	print e, frec_col[e]
	#quit()
	for y in xrange(ys):
		for x in xrange(xs):
			pixel_value = pixels[x, y][0]
			new_pixel_value = ()
			if pixel_value <= min_value:
				new_pixel_value = (0, 0, 0)
			elif pixel_value >= max_value:
				new_pixel_value = (255, 255, 255)
			else:
				aux = 255 * (pixel_value - min_value) / range_value
				new_pixel_value = (aux, aux, aux)
			new_pixels[x, y] = new_pixel_value
	return new_image

def find_gradients(image, mask_to_use, bool_normalize):
	mask = masks.define_mask(mask_to_use)
	if mask is None:
		print "Not define mask"
		quit()
	else:
		if __name__ == '__main__':
			print "Mask to use"
			print "\t", mask[0]
			print "\t", mask[1]
	mask_x, mask_y = mask[0], mask[1]
	gradients_x = masks.mask_pixel_operator(image, mask_x, bool_normalize)
	gradients_y = masks.mask_pixel_operator(image, mask_y, bool_normalize)
	xs, ys = image.size
	gradients = {}
	for gradient_key in gradients_x: #gradient_key -> (y, x)
		x_value, y_value = gradients_x[gradient_key], gradients_y[gradient_key]
		gradient_value = math.sqrt(math.pow(x_value, 2) + math.pow(y_value, 2))
		gradient_angle = math.atan2(x_value, y_value)
		slope_angle = math.atan2(y_value, x_value) #i hope that i don't cause any bug
		if gradient_key not in gradients:
			gradients[gradient_key] = [gradient_value, gradient_angle, y_value, x_value, slope_angle]
	return gradients
	
def adaptative_threshold(ys, xs, gradients):
	size_list = xs * ys
	list_gradients = []
	list_edges = [0] * size_list
	list_pixels = {}
	print len(list_edges)
	for x in xrange(xs):
		for y in xrange(ys):
			pixel_index = (y, x)
			gradient_value = gradients[pixel_index][0]
			list_gradients.append(gradient_value)
	print list_gradients
	quit()
	#First part
	square = xs / 8.0
	s = int(square/2.0)
	sum = 0.0
	threshold = 0.15
	for x in xrange(xs):
		sum = 0.0
		for y in xrange(ys):
			index_gradient = y *xs + 1
			sum = sum + list_gradients[index_gradient]
			if x == 0:
				list_edges[index_gradient] = sum
			else:
				list_edges[index_gradient] = list_edges[index_gradient-1] + sum
	for x in xrange(xs):
		for y in xrange(ys):
			index_gradient = y *xs + 1
			x1, x2, y1, y2 = (x - s), (x + s), (y - s), (y + s)
			if x1 < 0:
				x1 = 0
			if x2 >= xs:
				x2 = xs - 1
			if y1 < 0:
				y1 = 0
			if y2 >= ys:
				y2 = ys - 1
			count = (x2 - x1) * (y2 - y1)
			sum = list_edges[y2 * xs + x2] - list_edges[y1 * xs + x2] - list_edges[y2 * xs + x1] + list_edges[y1 * xs + x1]
			#print list_gradients[index_gradient], index_gradient
			if ((list_gradients[index_gradient] * count) < (sum * (1.0 - threshold))):
				list_pixels[(y, x)] = 0
			else:
				list_pixels[(y, x)] = 255
	miau = {}
	for key in list_pixels:
		value = list_pixels[key]
		if value not in miau:
			miau[value] = 0
		else:
			miau[value] += 1
	print miau
	quit()
	return None
	
def find_edges(image, mask_to_use, bool_normalize):
	gradients = find_gradients(image, mask_to_use, bool_normalize)
	white_color, black_color = (255, 255, 255), (0, 0, 0)
	xs, ys = image.size
	#adaptative_threshold(ys, xs, gradients)
	gradients_values = []
	for gradient_key in gradients:
		gradient_info = gradients[gradient_key]
		gradient_value = gradient_info[0]
		gradients_values.append(gradient_value)
	average_gradients = statistics.average(gradients_values)
	deviation_gradients = statistics.standard_deviation(gradients_values) / 2.0
	mode = statistics.mode(gradients_values)
	threshold = average_gradients
	edge_gradients = {}
	for gradient_key in gradients:
		gradient_info = gradients[gradient_key]
		gradient_value = gradient_info[0]
		gradient_angle = gradient_info[1]
		if gradient_value >= threshold:
			edge_gradients[gradient_key] = gradient_info
	return edge_gradients
	
def draw_edges(image, edge_gradients, bool_new):
	black_color = (0, 0, 0)
	pixels = image.load()
	if bool_new:
		image = Image.new("RGB", image.size, "white")
		pixels = image.load()
	for gradient_key in edge_gradients:
		y, x = gradient_key
		pixels[x, y] = black_color
	return image

#https://www.daniweb.com/software-development/python/code/216637/resize-an-image-python
def define_edges(image, mask_to_use):
	rgb_image = image.convert('RGB')
	gray_image = pix.grayscale_image(rgb_image)
	xs, ys = image.size
	total_pixels = xs * ys
	factor = 1
	if total_pixels < 22500:
		factor = 1.8
	elif total_pixels < 22500 and total_pixels > 16000:
		factor = 0.5
	elif total_pixels > 16000:
		factor = 0.5
	resize_image = pix.resize_image(gray_image, factor)
	for dummy in xrange(3):
		image = filters.filter_operator(resize_image, 'median')
	bool_normalize = False
	edge_gradients = find_edges(image, mask_to_use, bool_normalize)
	edge_image = draw_edges(image, edge_gradients, True) #new image
	return edge_image

def __main__(filename, choice_mask, choice_save):
	if choice_mask[0]:
		mask_to_use = choice_mask[1]
	else:
		mask_to_use = "sobeldg" #default
	original_image = Image.open(filename)
	edge_image = define_edges(original_image, mask_to_use)
	edge_image.show()
	if choice_save[0]:
		bool_save =  files.validate_save("edges\output\\", choice_save[1], '.png')
		if bool_save[0]:
			print "Directory of the new image: {}".format(bool_save[1])
			edge_image.save(bool_save[1])
	return None

#run in the 'package' directory
if __name__ == '__main__':
	pre_options = files.validate_arguments(sys.argv)
	__main__(pre_options[0], pre_options[1], pre_options[2])
