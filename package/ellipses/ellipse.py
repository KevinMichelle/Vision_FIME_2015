import sys
import random
import math
from PIL import Image, ImageDraw
import edges.edge as edge
import shapes.shape as shape
import utilities.files as files
import utilities.pix as pix
import utilities.structures as structures
import utilities.statistics as statistics
import utilities.neighbors as neighbors
import utilities.voting as voting
import lines.line as line
import utilities.gradients_angles as gradients_angles
import datetime

#http://en.wikipedia.org/wiki/Slope Slope info / Info de pendientes
#http://www.aishack.in/tutorials/converting-lines-from-normal-to-slopeintercept-form/ Normal form equation to slope equation
#http://www.math.com/tables/trig/identities.htm Identities
#http://en.wikipedia.org/wiki/Line%E2%80%93line_intersection Line-line intersection
#https://www.mathsisfun.com/algebra/trig-cosine-law.html
#https://www.mathsisfun.com/algebra/trig-solving-sss-triangles.html

def define_ellipses(image):
	mask_to_use = "prewittdg"
	shape_image_info = shape.floodfill(image, True)
	shape_image, shape_info = shape_image_info[0], shape_image_info[1]
	gradients = edge.find_edges(shape_image, mask_to_use, False)
	pixels = shape_image.load()
	xs, ys = shape_image.size
	y_center, x_center = int((ys / 2.0)), int((xs / 2.0))
	for shape_info_key in shape_info: #maybe i can move this for to a general function
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
		min_distance = statistics.euclidean_distance((upper_y, upper_x), (lower_y, lower_x)) / 2.0
		edge_pixels_key = structures.dict_to_list(edge_shape, True, True)
		edge_sample_list = random.sample(edge_shape, 16)
		voting_pixels_dict = {}
		ignore_pair_pixels = []
		for edge_sample in edge_sample_list:
			find_voting_pixels_ellipse(edge_sample, edge_shape, min_distance, ys, xs, pixels, bounding_box, voting_pixels_dict, ignore_pair_pixels)
		center = voting.voting_process(voting_pixels_dict, pixels, ys, xs)
		draw_ellipse(center, pixels, ys, xs)
	return shape_image

	
def draw_ellipse(center, pixels, ys, xs):
	white, red = (255, 255, 255), (255, 0, 0)
	yc, xc = center
	point_a = ()
	point_b = ()
	for y in xrange(yc, 0, -1):
		if pixels[xc, y] == white:
			point_a = (y + 1, xc)
			break
	for x in xrange(xc, xs):
		if pixels[x, yc] == white:
			point_b = (yc, x - 1)
			break
	distance_a = statistics.euclidean_distance(center, point_a)
	distance_b = statistics.euclidean_distance(center, point_b)
	semi_major_axis, semi_minor_axis = 0.0, 0.0
	if distance_a >= distance_b:
		semi_major_axis = distance_b
		semi_minor_axis = distance_a
	else:
		semi_major_axis = distance_b
		semi_minor_axis = distance_a
	limit = math.pow(semi_minor_axis, 2)
	x = (limit * (-1.0))
	while x <= limit:
		#x = pix.getXCoordinate(xpi, xc * 2.0)
		xpi = pix.getXPixel(x, xc * 2.0)
		aux1 = math.pow(x, 2)
		aux2 = math.pow(semi_major_axis, 2)
		aux3 = math.pow(semi_minor_axis, 2)
		aux4 = aux1/aux2
		aux5 = (1 - aux4) * aux3
		if aux5 >= 0.0:
			y1 = math.sqrt(aux5)
			y2 = (-1.0) * y1
			ypix1 = pix.getYPixel(y1, yc * 2.0)
			ypix2 = pix.getYPixel(y2, yc * 2.0)
			if ypix1 >= 0 and ypix1 < ys:
				pixels[xpi, ypix1] = red
			if ypix2 >= 0 and ypix2 < ys:
				pixels[xpi, ypix2] = red
		x += 0.0001
	return None
	
	
def find_voting_pixels_ellipse(edge_pixel, edge_shape, min_distance, ys, xs, pixels, bounding_box, voting_pixels_dict, ignore_pair_pixels):
	ya, xa = edge_pixel
	for edge_key in edge_shape:
		if edge_pixel > edge_key:
			check_pair = (edge_pixel, edge_key)
		else:
			check_pair = (edge_key, edge_pixel)
		if check_pair not in ignore_pair_pixels:
			ignore_pair_pixels.append(check_pair)
			yb, xb = edge_key
			distance = statistics.euclidean_distance((ya, xa), (yb, xb))
			if distance > min_distance:
				angle_a, angle_b = edge_shape[edge_pixel][4], edge_shape[edge_key][4] #slope
				pa, pb = line.define_line_p(ya, xa, angle_a, ys, xs), line.define_line_p(yb, xb, angle_b, ys, xs)
				info_first, info_second = (pa, ya, xa, angle_a), (pb, yb, xb, angle_b) 
				yp, xp = line.find_intersection(info_first, info_second, ys, xs)
				if yp is not None and xp is not None:
					point_a = (info_first[1], info_first[2])
					point_b = (info_second[1], info_second[2])
					point_c = (yp, xp)
					point_d = line.define_midpoint(point_a, point_b, ys, xs)
					line_pixels = line.get_pixels_line_slope(point_c, point_d, ys, xs, pixels, True)
					voting.update_pixels_voting(bounding_box, pixels, line_pixels, voting_pixels_dict) #update the total_voting_pixels dictionary
	return None
	

def __main__(filename, choice_info, choice_save):
	bool_info = False
	choice_info = False #dummy
	original_image = Image.open(filename)
	ellipse_image = define_ellipses(original_image)
	ellipse_image.show()
	if choice_save[0]:
		bool_save =  files.validate_save("ellipses\output\\", choice_save[1], '.png')
		if bool_save[0]:
			print "Directory of the new image: {}".format(bool_save[1])
			ellipse_image.save(bool_save[1])			
	return None
		
	
#run in the 'package' directory
if __name__ == '__main__':
	pre_options = files.validate_arguments(sys.argv)
	__main__(pre_options[0], pre_options[1], pre_options[2])
