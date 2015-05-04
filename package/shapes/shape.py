from PIL import Image, ImageDraw
import sys
import math
import random
import colorsys
import edges.edge as edge
import utilities.files as files
import utilities.pix as pix
import utilities.masks as masks
import utilities.neighbors as neighbors
import utilities.colors as colors
import utilities.bfs as bfs

#http://effbot.org/imagingbook/imagedraw.htm
def draw_shapes_info(image, shapes_info, bool_dummy): #duh name
	if bool_dummy:
		color_to_use = (30, 30, 30) #almost black color
	else:
		color_to_use = (255, 0, 0)
	pixels = image.load()
	xs, ys = image.size
	total = xs * ys
	print
	counter = 0
	for shape_key in shapes_info:
		info = shapes_info[shape_key]
		shape_limits, shape_center, shape_size, shape_color = info[0], info[1], info[2], shape_key #shape_key -> color
		percentage = round((float(shape_size) * 100.0) / float(total), 2)
		if percentage > 0.0:
			y1, y2 = shape_limits[0]
			x1, x2 = shape_limits[1]
			pix1, pix2, pix3, pix4 = (x1, y1), (x1, y2), (x2, y1), (x2, y2)
			draw = ImageDraw.Draw(image)
			draw.line((pix1, pix3), fill = color_to_use)
			draw.line((pix1, pix2), fill = color_to_use)
			draw.line((pix4, pix2), fill = color_to_use)
			draw.line((pix4, pix3), fill = color_to_use)
			draw_center_mass(image, shape_center)
			center_y, center_x = shape_center[0], shape_center[1]
			text = None
			if bool_dummy:
				text = "{} %".format(percentage)
			else:
				text = "{}".format(counter)
				counter += 1
			draw.text((center_x, center_y), text, fill=color_to_use)				
			print "Figure with color {}, center of mass {}, percentage in the image {}%".format(shape_color, shape_center, percentage)
	return image
	
#http://stackoverflow.com/a/22620206
def center_of_mass(image, pixel_list):
	sum_y, sum_x = 0, 0
	len_pixels = len(pixel_list)
	for pixel in pixel_list:
		sum_y += pixel[0]
		sum_x += pixel[1]
	return (sum_y/len_pixels, sum_x/len_pixels)
	
def find_shape_limits(pixels_list):
	y, x = [], []
	for pixel in pixels_list:
		y.append(pixel[0])
		x.append(pixel[1])
	y.sort()
	x.sort()
	y_ = (y[0], y[len(y) - 1])
	x_ = (x[0], x[len(x) - 1])
	return (y_, x_)
	
def draw_center_mass(image, center):
	black_color = (30, 30, 30) #almost black color
	xs, ys = image.size
	pixels = image.load()
	y, x = center[0], center[1]
	parameters, axis_limits = None, (ys, xs)
	neighbors_center = neighbors.find_neighbors(pixels, center, parameters, axis_limits)
	for neighbor_center in neighbors_center:
		dy, dx = neighbor_center[0]
		pixels[dx, dy] = black_color
	return None

def floodfill(image, bool_edge, objetivecolor):
	edge_image = None
	if bool_edge:
		mask_to_use = "prewittdg"
		edge_image = edge.define_edges(image, mask_to_use) #enhance edges
		edge_image = pix.enhance_pixels(edge_image)
	else:
		edge_image = image.copy()
	white_color, black_color = (255, 255, 255), (0, 0, 0)
	xs, ys = edge_image.size
	pixels = edge_image.load()
	colors_list = []
	max_color_counter = 0
	background_new_color = ()
	shapes_info = {}
	for y in xrange(ys):
		for x in xrange(xs):
			pixel_value = pixels[x, y]
			pixel = (y, x)
			if pixel_value == objetivecolor:
				visited_pixel = {}
				newcolor = ()
				if bool_edge and False: #i need to add a new option to choose the generator of colors
					newcolor = colors.color_generator(colors_list)
				else:
					newcolor = colors.lazy_generator(colors_list)
				colors_list.append(newcolor)
				visited_pixel[(y, x)] = 1
				queue_neighbors = list()
				queue_neighbors.append(pixel)
				while len(queue_neighbors) > 0:
					bfs.bfs(edge_image, queue_neighbors, objetivecolor, newcolor, visited_pixel)
				if bool_edge:
					if len(visited_pixel) > max_color_counter:
						background_new_color = newcolor
						max_color_counter = len(visited_pixel)
				if len(visited_pixel) > 0:
					new_center_mass = center_of_mass(edge_image, visited_pixel)
					shape_limits = find_shape_limits(visited_pixel)
					shapes_info[newcolor] = (shape_limits, new_center_mass, len(visited_pixel))
	if background_new_color in shapes_info:
		del shapes_info[background_new_color]
	image_size = (ys, xs)
	pix.change_color(pixels, background_new_color, white_color, image_size)
	pix.change_color(pixels, black_color, white_color, image_size)
	return edge_image, shapes_info

	
def define_shape(image, bool_info):
	whitecolor = (255, 255, 255)
	shape_image_info = floodfill(image, True, whitecolor)
	shape_image, shape_info = shape_image_info[0], shape_image_info[1]
	if bool_info:
		shape_image = draw_shapes_info(shape_image, shape_info, True)
	return shape_image
	
def __main__(filename, choice_info, choice_save):
	bool_info = False
	if choice_info[0]:
		bool_info = True
	original_image = Image.open(filename)
	rgb_image = original_image.convert('RGB')
	image = pix.grayscale_image(rgb_image)
	shape_image = define_shape(image, bool_info)
	shape_image.show()
	if choice_save[0]:
		bool_save =  files.validate_save("shapes\output\\", choice_save[1], '.png')
		if bool_save[0]:
			print "Directory of the new image: {}".format(bool_save[1])
			shape_image.save(bool_save[1])			
	return None
	
#run in the 'package' directory
if __name__ == '__main__':
	pre_options = files.validate_arguments(sys.argv)
	__main__(pre_options[0], pre_options[1], pre_options[2])
