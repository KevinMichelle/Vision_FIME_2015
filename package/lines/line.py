from PIL import Image, ImageDraw
import sys
import math
import edges.edge as edge
import utilities.pix as pix
import utilities.files as files
import utilities.statistics as statistics
import utilities.structures as structures
import utilities.colors as colors
import utilities.neighbors as neighbors
import utilities.bfs as bfs
import utilities.gradients_angles as gradients_angles
	

#line function only
def define_line_angles(angles, threshold):
	new_angles = {}
	colors_list = []
	for angle in angles:
		counter = angles[angle]
		if counter > threshold:
			newcolor = colors.color_generator(colors_list)
			colors_list.append(newcolor)
			new_angles[angle] = newcolor
	return new_angles
	
def define_lines_gradients(gradients, angles):
	new_gradients = {}
	for gradient in gradients:
		angle = gradients[gradient][1]
		if angle in angles:
			new_gradients[gradient] = gradients[gradient]
	return new_gradients
	
def define_equation_line(image, central_point, gradients, angles):
	black_color, white_color = (0, 0, 0), (255, 255, 255)
	equation_line = {}
	pixels = image.load()
	for gradient in gradients: #gradient -> y, x
		oldy, oldx = gradient
		angle =  gradients[gradient][1]
		y, x = oldy - central_point[0], oldx - central_point[1]
		rho = abs(int(x*math.cos(angle) + y*math.sin(angle)))
		aux = angle, rho
		if aux not in equation_line:
			equation_line[aux] = 1
		else:
			equation_line[aux] += 1
		pixels[oldx, oldy] = angles[angle]
		if pixels[oldx, oldy] == black_color:
			pixels[oldx, oldy] = white_color
	print equation_line
	suma = 0
	miau = []
	for i in equation_line:
		miau.append(equation_line[i])
		suma += equation_line[i]
	print suma
	print miau, "hola"
	prom = statistics.average(miau)
	print prom
	nuevos = []
	for i in equation_line:
		if equation_line[i] >= prom:
			if i not in nuevos:
				nuevos.append(i)
	print nuevos
	print len(nuevos)
	for i in nuevos:
		print i
	parameters = 5, 5
	image.show()
	white_black = (True, True) #ignore white and black pixels in the neighborhood, only update white and black pixels
	image = pix.filter_pixels(image, white_black, True, "mode", parameters)
	image.show()
	white_black = (True, False)
	image = pix.filter_pixels(image, white_black, True, "mode", parameters)
	image.show()
	white_black = (True, True)
	image = pix.filter_pixels(image, white_black, True, "mode", parameters)
	image.show()
	image = pix.enhance_pixels(image, True)
	image.show()
	return image
	

	
def define_lines(image):
	mask_to_use = "prewittdg"
	gradients = edge.find_edges(image, mask_to_use, False)
	edge_image = edge.define_edges(image, mask_to_use, False)
	xs, ys = edge_image.size
	central_point = (ys/2.0), (xs/2.0)
	angles = gradients_angles.define_angles(gradients, 1)
	counter_angles = structures.dict_to_list(angles, False, False)
	average_counter = statistics.average(counter_angles)
	median_counter = statistics.median(counter_angles)
	new_angles = define_line_angles(angles, average_counter)
	lines_gradients = define_lines_gradients(gradients, new_angles)
	image = define_equation_line(edge_image, central_point, lines_gradients, new_angles)
	xs, ys = image.size
	pixels = image.load()
	colors_list = pix.colors_image(image)
	white_color, black_color = (255, 255, 255), (0, 0, 0)
	visited_pixels = {}
	image.show()
	for y in xrange(ys):
		for x in xrange(xs):
			pixel = (y, x)
			if pixel not in visited_pixels:
				pixel_value = pixels[x, y]
				if pixel_value != white_color:
					newcolor = colors.color_generator(colors_list)
					colors_list.append(newcolor)
					visited_pixels[(y, x)] = 1
					queue_neighbors = list()
					queue_neighbors.append(pixel)
					while len(queue_neighbors) > 0:
						bfs.bfs(image, queue_neighbors, pixel_value, newcolor, visited_pixels)
	return image

def __main__(filename, choice_info, choice_save):
	bool_info = False
	choice_info = False #dummy
	original_image = Image.open(filename)
	rgb_image = original_image.convert('RGB')
	image = pix.grayscale_image(rgb_image)
	lines_image = define_lines(image)
	lines_image.show()
	if choice_save[0]:
		bool_save =  files.validate_save("lines\output\\", choice_save[1], '.png')
		if bool_save[0]:
			print "Directory of the new image: {}".format(bool_save[1])
			lines_image.save(bool_save[1])			
	return None
	
def find_intersection(info_a, info_b, ys, xs):
	a, yap, xap, alfa = info_a[0], info_a[1], info_a[2], info_a[3]
	b, ybp, xbp, beta = info_b[0], info_b[1], info_b[2], info_b[3]
	ya, xa, yb, xb = pix.getYCoordinate(yap, ys), pix.getXCoordinate(xap, xs), pix.getYCoordinate(ybp, ys), pix.getXCoordinate(xbp, xs)
	aux = ((math.sin(alfa) * math.cos(beta)) - (math.sin(beta) * math.cos(alfa)))
	if aux != 0 and math.sin(alfa) != 0:
		x = (b * math.sin(alfa) - a * math.sin(beta)) / aux
		y = (a - x * math.cos(alfa)) / math.sin(alfa)
		yp, xp = pix.getYPixel(y, ys), pix.getXPixel(x, xs)
	else:
		yp,xp = None, None
	return (yp, xp)
	
def define_line_p(y, x, angle, ys, xs):
	y = pix.getYCoordinate(y, ys) #real coordinates
	x = pix.getXCoordinate(x, xs)
	cos_angle, sin_angle = math.cos(angle), math.sin(angle)
	p = (x * cos_angle) + (y * sin_angle)
	return p

def define_line_slope(point_a, point_b, ys, xs):
	ayp, axp = point_a
	byp, bxp = point_b
	ayc, axc, byc, bxc = pix.getYCoordinate(ayp, ys), pix.getXCoordinate(axp, xs), pix.getYCoordinate(byp, ys), pix.getXCoordinate(bxp, xs)
	if (axc - bxc) != 0:
		m = (ayc - byc)/(axc - bxc)
	else:
		m = None
	return m
	
def define_midpoint(point_a, point_b, ys, xs):
	ayp, axp = point_a
	byp, bxp = point_b
	ayc, axc, byc, bxc = pix.getYCoordinate(ayp, ys), pix.getXCoordinate(axp, xs), pix.getYCoordinate(byp, ys), pix.getXCoordinate(bxp, xs)
	yc = (ayc + byc)/2.0
	xc = (axc + bxc)/2.0
	yp, xp = pix.getYPixel(yc, ys), pix.getXPixel(xc, xs)
	return (yp, xp)
	
def get_pixels_line_normal(y, x, angle, ys, xs, pixels, ignore):
	white, black = (255, 255, 255), (0, 0, 0)
	p = define_line_p(y, x, angle, ys, xs)
	cos_angle, sin_angle = math.cos(angle), math.sin(angle)
	pixels_line = []
	if sin_angle != 0:
		for x_pixel in xrange(xs):
			x_new = pix.getXCoordinate(x_pixel, xs)
			y_new = (p / sin_angle) - ((x_new * cos_angle) / sin_angle)
			y_pixel = pix.getYPixel(y_new, ys)
			x_pixel = pix.getXPixel(x_new, xs)
			if y_pixel >= 0 and y_pixel < ys:
				if ignore:
					color_pixel = pixels[x_pixel, y_pixel]
					if color_pixel != white and color_pixel != black:
						pixels_line.append((y_pixel, x_pixel))
				else:
					pixels_line.append((y_pixel, x_pixel))
	else:
		for y_pixel in xrange(ys):
			pixels_line.append((y_pixel, x))
	return pixels_line
	
def get_pixels_line_slope(point_a, point_b, ys, xs, pixels, ignore):
	white, black, red = (255, 255, 255), (0, 0, 0), (255, 0, 0)
	slope = define_line_slope(point_a, point_b, ys, xs)
	pixels_line = []
	if slope is not None:
		yp, xp = point_a
		yc, xc = pix.getYCoordinate(yp, ys), pix.getXCoordinate(xp, xs)
		b = yc - (xc*slope)
		for x_pixel in xrange(xs):
			x_new = pix.getXCoordinate(x_pixel, xs)
			y_new = (slope*x_new) + b
			y_pixel = pix.getYPixel(y_new, ys)
			if ignore:
				if y_pixel >= 0 and y_pixel < ys:
						color_pixel = pixels[x_pixel, y_pixel]
						if color_pixel != white and color_pixel != black:
								pixels_line.append((y_pixel, x_pixel))
			else:
				pixels_line.append((y_pixel, x_pixel))
	return pixels_line
	
	
#run in the 'package' directory
if __name__ == '__main__':
	pre_options = files.validate_arguments(sys.argv)
	__main__(pre_options[0], pre_options[1], pre_options[2])
