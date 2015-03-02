from PIL import Image
import math
import utilities.neighbors as neighbors
import utilities.statistics as statistics

def filter_pixels(image, white_black, rgb, option, parameters):
	black_color, white_color = (0, 0, 0), (255, 255, 255)
	xs, ys = image.size
	pixels = image.load()
	axis_limits = (ys, xs)
	new_image = image.copy()
	new_pixels = new_image.load()
	for y in xrange(ys):
		for x in xrange(xs):
			pixel = (y, x)
			pixel_value = pixels[x, y]
			neighbor_pixels = neighbors.find_neighbors(pixels, pixel, parameters, axis_limits)
			neighbor_values = []
			for pixel_info in neighbor_pixels:
				if rgb:
					neighbor_pixel_value = pixel_info[1]
				else:
					neighbor_pixel_value = pixel_info[1][0]
				if white_black[0]:
					if neighbor_pixel_value != (255, 255, 255) and neighbor_pixel_value != (0, 0, 0):
						neighbor_values.append(neighbor_pixel_value)
				else:
					neighbor_values.append(neighbor_pixel_value)
			if rgb:
				red_values, green_values, blue_values = [], [], []
				new_red, new_green, new_blue = None, None, None
				for color in neighbor_values:
					red, green, blue = color[0], color[1], color[2]
					red_values.append(red)
					green_values.append(green)
					blue_values.append(blue)
				if len(red_values) > 0 and len(green_values) > 0 and len(blue_values) > 0:
					if option == "max":
						new_red = max(red_values)
						new_green = max(green_values)
						new_blue = max(blue_values)
					elif option == "mode":
						new_value = statistics.mode(neighbor_values)
						new_red, new_green, new_blue = new_value[0], new_value[1], new_value[2]
				if new_red is not None and new_green is not None and new_blue is not None:
					if white_black[1]:
						if pixel_value == white_color or pixel_value == black_color:
							new_pixels[x, y] = (new_red, new_green, new_blue)
					else:
						if pixel_value != white_color and pixel_value != black_color:
							new_pixels[x, y] = (new_red, new_green, new_blue)
						
			else:
				print "Por implementar"
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