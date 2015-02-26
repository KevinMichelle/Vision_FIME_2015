from PIL import Image

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