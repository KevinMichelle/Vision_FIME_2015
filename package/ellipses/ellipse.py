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
import utilities.gradients_angles as gradients_angles

#http://en.wikipedia.org/wiki/Slope Slope info / Info de pendientes
#http://www.aishack.in/tutorials/converting-lines-from-normal-to-slopeintercept-form/ Normal form equation to slope equation
#http://www.math.com/tables/trig/identities.htm Identities

def define_ellipses(image):
	mask_to_use = "prewittdg"
	shape_image_info = shape.floodfill(image)
	shape_image, shape_info = shape_image_info[0], shape_image_info[1]
	gradients = edge.find_edges(shape_image, mask_to_use, False)
	pixels = shape_image.load()
	xs, ys = shape_image.size
	y_center, x_center = int((ys / 2.0)), int((xs / 2.0))
	for shape_info_key in shape_info:
		print shape_info_key, "HOLA", shape_info[shape_info_key]
		info = shape_info[shape_info_key]
		y_shape, x_shape = info[0][0], info[0][1]
		print y_shape, x_shape
		lower_y, upper_y = y_shape[0], y_shape[1]
		lower_x, upper_x = x_shape[0], x_shape[1]
		edge_shape = {}
		for y in xrange(lower_y, upper_y + 1):
			for x in xrange(lower_x, upper_x + 1):
				check = (y, x)
				if check in gradients:
					edge_shape[check] = gradients[check]
		if len(edge_shape) == 0:
			print "Weird bug"
			break
		angles = gradients_angles.define_angles(edge_shape, 3)
		for edge_pixel in edge_shape:
			draw_line_pixel(edge_shape[edge_pixel], edge_pixel, pixels, ys, xs)
			shape_image.show()
			second_pixel = random.choice(edge_shape.keys())
			print edge_pixel, second_pixel 
			while edge_pixel == second_pixel:
				second_pixel = random.choice(edge_shape.keys())
			print edge_pixel, second_pixel
			draw_line_pixel(edge_shape[second_pixel], second_pixel, pixels, ys, xs)
			shape_image.save("ellipses\output\incomplete.png")
			quit()
		print "CENTER, RADIUS"
		print "\n"
	quit()
	return shape_image
	
def draw_line_pixel(pixel_info, pixel_key, pixels, ys, xs):
	y_aux, x_aux = pixel_key #pixel coordinates
	y = int(round((ys / 2) - y_aux)) #real coordinates
	x = int(round(x_aux - (xs / 2))) #real coordinates
	g = pixel_info[0]
	gy = pixel_info[2]
	gx = pixel_info[3]
	#edge_angle = edge_shape[edge_pixel][1]
	angle = pixel_info[4] #slope_angle
	#angle = edge_shape[edge_pixel][1]
	cos_angle, sin_angle = math.cos(angle), math.sin(angle)
	p = (x * cos_angle) + (y * sin_angle)
	if angle != 0:
		for x_pixel in xrange(xs):
			x_new = int(round(x_pixel - (xs / 2)))
			y_new = (p - (x_new * cos_angle)) / sin_angle
			y_pixel = int(round((ys/2.0) - y_new)) #acoordin to the pixels coordinates
			if y_pixel >= 0 and y_pixel < ys:
				pixels[x_pixel, y_pixel] = (255, 0, 0)
	else:
		for y_pixel in xrange(ys):
			pixels[x_aux, y_pixel] = (255, 0, 0)

def __main__(filename, choice_info, choice_save):
	bool_info = False
	choice_info = False #dummy
	original_image = Image.open(filename)
	rgb_image = original_image.convert('RGB')
	image = pix.grayscale_image(rgb_image)
	circle_image = define_ellipses(image)
	circle_image.show()
	if choice_save[0]:
		bool_save =  files.validate_save("ellipses\output\\", choice_save[1], '.png')
		if bool_save[0]:
			print "Directory of the new image: {}".format(bool_save[1])
			circle_image.save(bool_save[1])			
	return None
	
def draw_ellipse():
	return None;

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