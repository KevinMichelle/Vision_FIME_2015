import sys
import random
from PIL import Image, ImageDraw
import edges.edge as edge
import shapes.shape as shape
import utilities.files as files
import utilities.pix as pix
import utilities.structures as structures
import utilities.statistics as statistics
import utilities.gradients_angles as gradients_angles

def define_circles(image):
	mask_to_use = "prewittdg"
	shape_image_info = shape.floodfill(image)
	shape_image, shape_info = shape_image_info[0], shape_image_info[1]
	gradients = edge.find_edges(shape_image, mask_to_use, False)
	shape_image = edge.draw_edges(shape_image, gradients, False)
	pixels = shape_image.load()
	xs, ys = shape_image.size
	y_center, x_center = int((ys / 2.0)), int((xs / 2.0))
	shape_image = shape.draw_shapes_info(shape_image, shape_info)
	for shape_info_key in shape_info:
		accumulator = {}
		info = shape_info[shape_info_key]
		y_shape, x_shape = info[0][0], info[0][1]
		center = info[1]
		print y_shape, x_shape, center
		lower_y, upper_y = y_shape[0], y_shape[1]
		lower_x, upper_x = x_shape[0], x_shape[1]
		edge_shape = {}
		for y in xrange(lower_y - 1, upper_y + 2):
			for x in xrange(lower_x - 1, upper_x + 2):
				check = (y, x)
				if check in gradients:
					edge_shape[check] = gradients[check]
		if len(edge_shape) == 0:
			print "Weird bug"
			break
		angles = gradients_angles.define_angles(edge_shape, 2)
		frec_angles = structures.dict_to_list(angles, False, False)
		average_frec_angle = statistics.average(frec_angles)
		standard_deviation_frec_angle = statistics.standard_deviation(frec_angles)
		if average_frec_angle > standard_deviation_frec_angle:
			print "\nMAYBE THIS SHAPE IS A CIRCLE"
			for edge_pixel in edge_shape:
				y_aux, x_aux = edge_pixel #pixel coordinates
				y = int(round((ys / 2) - y_aux)) #real coordinates
				x = int(round(x_aux - (xs / 2))) #real coordinates
				g = edge_shape[edge_pixel][0]
				gy = edge_shape[edge_pixel][2]
				gx = edge_shape[edge_pixel][3]
				cos_angle, sin_angle = (gx/g), (gy/g)
				radius = statistics.euclidean_distance(center, edge_pixel)
				y_circle_aux, x_circle_aux = int((y - (radius * sin_angle))), int((x - (radius * cos_angle))) #according the origin in a cartesian plane
				y_circle = int(round((ys/2.0) - y_circle_aux)) #acoordin to the pixels coordinates
				x_circle = int(round(x_circle_aux + (xs/2.0))) #acoordin to the pixels coordinates
				key_accumulator = (y_circle, x_circle)
				if (y_circle >= 0 and y_circle < ys) and (x_circle >= 0 and x_circle < xs):
					pixels[x_circle, y_circle] = (255, 0, 0)
				if key_accumulator not in accumulator:
					accumulator[key_accumulator] = 1
				else:
					accumulator[key_accumulator] += 1
			center_circle = center_of_circle(accumulator, shape_info)
			print "CENTER, RADIUS"
			print center_circle, radius
			shape_image = draw_circle(shape_image, center, radius)
		print "\n"
	return shape_image

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
def draw_circle(image, center, radius):
	color_sample = (0, 255, 0)
	draw = ImageDraw.Draw(image)
	y, x = center[0], center[1]
	draw.ellipse((x - radius, y - radius, x + radius, y + radius), fill = None, outline = color_sample)
	return image

#http://stackoverflow.com/a/306417
def center_of_circle(accumulator, shape_info):
	y_values, x_values = [], []
	for element in accumulator:
		y_sample = element[0]
		x_sample = element[1]
		if y_sample not in y_values:
			y_values.append(y_sample)
		if x_sample not in x_values:
			x_values.append(x_sample)
	y_average = int(statistics.average(y_values))
	x_average = int(statistics.average(x_values))
	return (y_average, x_average)
		
	
#run in the 'package' directory
if __name__ == '__main__':
	pre_options = files.validate_arguments(sys.argv)
	__main__(pre_options[0], pre_options[1], pre_options[2])