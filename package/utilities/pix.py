from PIL import Image
import math
import utilities.neighbors as neighbors
import utilities.statistics as statistics

#https://www.daniweb.com/software-development/python/code/216637/resize-an-image-python
def resize_image(image, factor):
	xs, ys = image.size
	ys, xs = int(ys * factor), int(xs * factor)
	new_image = image.resize((xs, ys), Image.ANTIALIAS)
	return new_image

def enhance_pixels(image, bool_control):
	black_color, white_color = (0, 0, 0), (255, 255, 255)
	pixels = image.load()
	xs, ys = image.size
	new_image = image.copy()
	new_pixels = new_image.load()
	control = 2
	if bool_control:
		parameters = 7, 7
	else:
		parameters = 3, 3
	axis_limits = (ys, xs)
	for y in xrange(ys):
		for x in xrange(xs):
			pixel = (y, x)
			pixel_value = pixels[x, y]
			counter = 0
			neighbor_pixels = neighbors.find_neighbors(pixels, pixel, parameters, axis_limits)
			for pixel_info in neighbor_pixels:
				neighbor_pixel_value = pixel_info[1][0]
				if neighbor_pixel_value == black_color[0]:
					counter += 1
			if pixel_value == white_color and bool_control: #(255, 255, 255) and True
				if counter > control:
					new_pixels[x, y] = black_color #add edge pixels
	return new_image

def change_color(pixels, oldcolor, newcolor, image_size):
	ys, xs = image_size
	for y in xrange(ys):
		for x in xrange(xs):
			if y >= 0 and y < ys:
				if x >= 0 and x < xs:
					color = pixels[x, y]
					if oldcolor is None and newcolor is None:
						if not color == (0, 0, 0):
							pixels[x, y] = (255, 255, 255)
					else:
						if color == oldcolor:
							pixels[x, y] = newcolor
	return None
	
def colors_image(image):
	xs, ys = image.size
	pixels = image.load()
	colors = []
	for y in xrange(ys):
		for x in xrange(xs):
			pixel_value = pixels[x, y]
			if pixel_value not in colors:
				colors.append(pixel_value)
	return colors
	
def frec_colors(image):
	frec = {}
	list_of_colors = colors_image(image)
	xs, ys = image.size
	pixels = image.load()
	for y in xrange(ys):
		for x in xrange(xs):
			pixel_value = pixels[x, y]
			if pixel_value in list_of_colors:
				if pixel_value not in frec:
					frec[pixel_value] = 1
				else:
					frec[pixel_value] += 1
	return frec
	
def max_color(image, frec_colors):
	aux = 0
	max_color_list = []
	for color in frec_colors:
		frec = frec_colors[color]
		if frec > aux:
			aux = frec
	for color in frec_colors:
		frec = frec_colors[color]
		if frec == aux:
			max_color_list.append(color)
	return max_color_list
	
def grayscale_image(image):
	xs, ys = image.size
	pixels = image.load()
	new_image = image.copy()
	new_pixels = new_image.load()
	for y in xrange(ys):
		for x in xrange(xs):
			pixel = pixels[x, y]
			average = (pixel[0] + pixel[1] + pixel[2]) / 3
			new_pixels[x, y] = (average, average, average)
	return new_image
	
def change_pixels(image, pixels):
	new_image = image.copy()
	new_pixels = new_image.load()
	for pixel_coordinates in pixels:
		pixel_value = pixels[pixel_coordinates]
		y, x = pixel_coordinates
		new_pixels[x, y] = (pixel_value, pixel_value, pixel_value)
	return new_image
	
def draw_pixels_color(list_of_pixels, pixels, color, ys, xs):
	for pix in list_of_pixels:
		y, x = pix
		if y >= 0 and y <ys and x >= 0 and x < xs:
			pixels[x, y] = color
	return None
	
def draw_point(point, pixels):
	if point is not None:
		if len(point) == 2:
			y, x = point
			pixels[x, y] = (255, 0, 0)
	return None
	
def getYCoordinate(y, ys):
	new_y = float((ys/2.0) - y)
	return new_y

def getXCoordinate(x, xs):
	new_x = float(x - (xs/2.0))
	return new_x
	
def getYPixel(y, ys):
	new_y = int((ys/2.0) - y)
	return new_y

def getXPixel(x, xs):
	new_x = int(x + (xs/2.0))
	return new_x