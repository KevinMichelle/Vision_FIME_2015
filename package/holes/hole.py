import sys
import random
import math
from PIL import Image, ImageDraw
import edges.edge as edge
import shapes.shape as shape
import utilities.files as files
import utilities.statistics as statistics
import utilities.pix as pix

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
	
def define_histogram(image, bool_plane): #if bool_plane is true, then it is horizontal histogram, else it is vertical
	xs, ys = image.size
	pixels = image.load()
	histogram = {}
	main_max = 0
	other_max = 0
	if bool_plane:
		main_max = ys
		other_max = xs
	else:
		main_max = xs
		other_max = ys
	for main_pos in xrange(main_max):
		list_of_values = []
		for other_pos in xrange(other_max):
			y, x = 0, 0
			if bool_plane:
				y = main_pos
				x = other_pos
			else:
				y = other_pos
				x = main_pos
			value = pixels[x, y][0]
			list_of_values.append(value)
		histogram[main_pos] = list_of_values
	return histogram
	
def find_possible_holes(histogram, bool_plane): #the developer must be aware of the plane of the histogram
	possible_holes = []
	for main_pos in histogram:
		histo = histogram[main_pos]
		average = statistics.average(histo)
		deviation = statistics.standard_deviation(histo)
		threshold = deviation * 3
		for other_pos in xrange(len(histo)):
			y, x = 0, 0
			value = histo[other_pos]
			if value < threshold:
				if bool_plane:
					y = main_pos
					x = other_pos
				else:
					y = other_pos
					x = main_pos
				possible_holes.append((y, x))
	return possible_holes
	
def image_holes(image, horizontal_holes, vertical_holes):
	red = (255, 0, 0)
	white, black = (255, 255, 255), (0, 0, 0)
	xs, ys = image.size
	new_image = Image.new("RGB", (xs, ys), "white")
	new_pixels = new_image.load()
	for hole in horizontal_holes:
		y, x = hole
		new_pixels[x, y] = red
	for hole in vertical_holes:
		y, x = hole
		pixel_value = new_pixels[x, y]
		if pixel_value == red:
			new_pixels[x, y] = black
	for y in xrange(ys):
		for x in xrange(xs): 
			pixel_value = new_pixels[x, y]
			if pixel_value == red:
				new_pixels[x, y] = white
	return new_image
	
def check_size_holes(shapes_info):
	new_shapes_Info = {}
	list_of_sizes = []
	print list_of_sizes
	shapes_to_delete = []
	for color in shapes_info:
		size_shape = shapes_info[color][2]
		if size_shape not in list_of_sizes:
			list_of_sizes.append(size_shape)
	average_size = statistics.average(list_of_sizes)
	deviation_size = statistics.standard_deviation(list_of_sizes)
	threshold  = int(average_size - (deviation_size))
	for color in shapes_info:
		size_shape = size_shape = shapes_info[color][2]
		if size_shape < threshold:
			shapes_to_delete.append(color)
	for shape_color in shapes_to_delete:
		if shape_color in shapes_info:
			del shapes_info[shape_color]
	return None

def define_holes(image):
	mask_to_use = "prewittdg"
	image = pix.grayscale_image(image) #replace the image object
	xs, ys = image.size #remove later
	bin_image = binarized_image(image)
	horizontal_histogram = define_histogram(image, True)
	vertical_histogram = define_histogram(image, False)
	horizontal_holes = find_possible_holes(horizontal_histogram, True)
	vertical_holes = find_possible_holes(vertical_histogram, False)
	img_holes = image_holes(image, horizontal_holes, vertical_holes)
	shape_img_holes, shapes_info_holes = shape.floodfill(img_holes, False)
	if shapes_info_holes is None:
		print "Error"
		quit()
	check_size_holes(shapes_info_holes)
	holes_image = shape.draw_shapes_info(image, shapes_info_holes, False)
	return holes_image


def __main__(filename, choice_info, choice_save):
	bool_info = False
	choice_info = False #dummy
	original_image = Image.open(filename)
	hole_image = define_holes(original_image)
	if choice_save[0]:
		bool_save =  files.validate_save("holes\output\\", choice_save[1], '.png')
		if bool_save[0]:
			print "Directory of the new image: {}".format(bool_save[1])
			hole_image.save(bool_save[1])			
	return None
		
	
#run in the 'package' directory
if __name__ == '__main__':
	pre_options = files.validate_arguments(sys.argv)
	__main__(pre_options[0], pre_options[1], pre_options[2])
