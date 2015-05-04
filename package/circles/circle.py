import sys
import random
import math
from PIL import Image, ImageDraw
import edges.edge as edge
import shapes.shape as shape
import lines.line as line
import utilities.files as files
import utilities.pix as pix
import utilities.structures as structures
import utilities.statistics as statistics
import utilities.voting as voting
import utilities.pix as pix
import utilities.gradients_angles as gradients_angles

#Hello

def define_circles(image):
	mask_to_use = "prewittdg"
	whitecolor = (255, 255, 255)
	shape_image_info = shape.floodfill(image, True, whitecolor)
	shape_image, shape_info = shape_image_info[0], shape_image_info[1]
	gradients = edge.find_edges(shape_image, mask_to_use, False)
	pixels = shape_image.load()
	xs, ys = shape_image.size
	y_center, x_center = int((ys / 2.0)), int((xs / 2.0))
	for shape_info_key in shape_info:
		info = shape_info[shape_info_key]
		y_shape, x_shape = info[0][0], info[0][1]
		lower_y, upper_y = y_shape[0], y_shape[1]
		lower_x, upper_x = x_shape[0], x_shape[1]
		bounding_box = (y_shape, x_shape)
		edge_shape = {}
		color_shape = shape_info_key
		for y in xrange(lower_y, upper_y + 1):
			for x in xrange(lower_x, upper_x + 1):
				check = (y, x)
				if check in gradients:
					edge_shape[check] = gradients[check]
		if len(edge_shape) == 0:
			print "Weird bug"
			break
		gradients_angles.define_angles(gradients, 3) #discretize angles of gradients, check later
		max_distance = statistics.euclidean_distance((upper_y, upper_x), (lower_y, lower_x)) / 2.0
		min_distance = statistics.euclidean_distance((lower_y, lower_x), (lower_y, upper_x)) / 2.0
		voting_pixels_dict = {}
		for edge_sample in edge_shape:
			y, x = edge_sample
			angle = edge_shape[edge_sample][1]
			find_voting_pixels_circle(y, x, angle, min_distance, max_distance, ys, xs, pixels, voting_pixels_dict, color_shape)
		center = voting.voting_process(voting_pixels_dict, pixels, ys, xs)
		draw_circle(center, pixels, ys, xs, shape_image)
		print center
	return shape_image

def find_voting_pixels_circle(y, x, angle, min_distance, max_distance, ys, xs, pixels, voting_pixels_dict, color_shape):
	discret_counter = min_distance
	alt_angle = (angle + (math.pi)) % (math.pi*2.0)
	angles_circle = (angle, alt_angle)
	line_pixels = []
	while discret_counter <= max_distance:
		for angle_circle in angles_circle:
			yc, xc = pix.getYCoordinate(y, ys), pix.getXCoordinate(x, xs)
			cos_angle, sin_angle = math.cos(angle_circle), math.sin(angle_circle)
			ycc, xcc = (yc - (discret_counter * sin_angle)), (xc - (discret_counter * cos_angle))
			ycp, xcp = pix.getYPixel(ycc, ys), pix.getXPixel(xcc, xs)
			possible_center = (ycp, xcp)
			if ycp >= 0 and ycp < ys and xcp >= 0 and xcp < xs:
				pixel_value = pixels[xcp, ycp]
				if pixel_value == color_shape:
					if possible_center not in voting_pixels_dict:
						voting_pixels_dict[possible_center] = 1
					else:
						voting_pixels_dict[possible_center] += 1
			else:
					if possible_center not in voting_pixels_dict:
						voting_pixels_dict[possible_center] = 1
					else:
						voting_pixels_dict[possible_center] += 1
		discret_counter += 0.01
	#voting.update_pixels_voting(bounding_box, pixels, line_pixels, voting_pixels_dict)
	return None

def __main__(filename, choice_info, choice_save):
	bool_info = False
	choice_info = False #dummy
	original_image = Image.open(filename)
	rgb_image = original_image.convert('RGB')
	image = pix.grayscale_image(rgb_image)
	circle_image = define_circles(image)
	circle_image.show()
	if choice_save[0]:
		bool_save =  files.validate_save("circles\output\\", choice_save[1], '.png')
		if bool_save[0]:
			print "Directory of the new image: {}".format(bool_save[1])
			circle_image.save(bool_save[1])			
	return None
	
#http://stackoverflow.com/a/2980931
def draw_circle(center, pixels, ys, xs, image):
	white, red = (255, 255, 255), (255, 0, 0)
	yc, xc = center
	pixels[xc, yc] = (255, 0, 255)
	point_a = ()
	point_b = ()
	point_c = ()
	point_d = ()
	for y in xrange(yc, 0, -1):
		if pixels[xc, y] == white:
			point_a = (y + 1, xc)
			#pix.draw_point(point_a, pixels)
			break
	for x in xrange(xc, xs):
		if pixels[x, yc] == white:
			point_b = (yc, x - 1)
			#pix.draw_point(point_b, pixels)
			break
	for y in xrange(yc, ys):
		if pixels[xc, y] == white:
			point_c = (y - 1, xc)
			#pix.draw_point(point_c, pixels)
			break
	for x in xrange(xc, 0, - 1):
		if pixels[x, yc] == white:
			point_d = (yc, x + 1)
			#pix.draw_point(point_d, pixels)
			break
	distances = []
	if point_a is not None:
		distance = statistics.euclidean_distance(center, point_a)
		distances.append(distance)
	if point_b is not None:
		distance = statistics.euclidean_distance(center, point_b)
		distances.append(distance)
	if point_c is not None:
		distance = statistics.euclidean_distance(center, point_c)
		distances.append(distance)
	if point_d is not None:
		distance = statistics.euclidean_distance(center, point_d)
		distances.append(distance)
	radius = statistics.average(distances)
	limit = math.pow(radius, 2)
	x = (limit * (-1.0))
	while x <= limit:
		#x = pix.getXCoordinate(xpi, xc * 2.0)
		xpi = pix.getXPixel(x, xc * 2.0)
		aux1 = math.pow(radius, 2)
		aux2 = math.pow(x, 2)
		aux3 = aux1 - aux2
		if aux3 >= 0.0:
			y1 = math.sqrt(aux3)
			y2 = (-1.0) * y1
			ypix1 = pix.getYPixel(y1, yc * 2.0)
			ypix2 = pix.getYPixel(y2, yc * 2.0)
			if ypix1 >= 0.0 and ypix1 < ys and xpi >= 0 and xpi < xs:
				pixels[xpi, ypix1] = red
			if ypix2 >= 0.0 and ypix2 < ys and xpi >= 0 and xpi < xs:
				pixels[xpi, ypix2] = red
		x += 0.01
	return None
	
#run in the 'package' directory
if __name__ == '__main__':
	pre_options = files.validate_arguments(sys.argv)
	__main__(pre_options[0], pre_options[1], pre_options[2])