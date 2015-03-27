from PIL import Image
import sys
import os.path
import random
import math
import utilities.files as files
import utilities.statistics as statistics
import utilities.pix as pix
import utilities.masks as masks

def find_gradients(image, mask_to_use, bool_normalize):
	mask = masks.define_mask(mask_to_use)
	if mask is None:
		print "Not define mask"
		quit()
	else:
		if __name__ == '__main__':
			print "Mask to use"
			print "\t", mask[0]
			print "\t", mask[1]
	mask_x, mask_y = mask[0], mask[1]
	gradients_x = masks.mask_pixel_operator(image, mask_x, bool_normalize)
	gradients_y = masks.mask_pixel_operator(image, mask_y, bool_normalize)
	xs, ys = image.size
	gradients = {}
	for gradient_key in gradients_x: #gradient_key -> (y, x)
		x_value, y_value = gradients_x[gradient_key], gradients_y[gradient_key]
		gradient_value = int(math.pow(abs(x_value) + abs(y_value), 2))
		gradient_angle = math.atan2(x_value, y_value)
		slope_angle = math.atan2(y_value, x_value) #i hope that i don't cause any bug
		if gradient_key not in gradients:
			gradients[gradient_key] = [gradient_value, gradient_angle, y_value, x_value, slope_angle]
	return gradients
	
def find_edges(image, mask_to_use, bool_normalize):
	gradients = find_gradients(image, mask_to_use, bool_normalize)
	white_color, black_color = (255, 255, 255), (0, 0, 0)
	gradients_values = []
	for gradient_key in gradients:
		gradient_info = gradients[gradient_key]
		gradient_value = gradient_info[0]
		gradients_values.append(gradient_value)
	threshold = statistics.average(gradients_values)
	edge_gradients = {}
	for gradient_key in gradients:
		gradient_info = gradients[gradient_key]
		gradient_value = gradient_info[0]
		gradient_angle = gradient_info[1]
		if gradient_value >= threshold:
			edge_gradients[gradient_key] = gradient_info
	return edge_gradients
	
def draw_edges(image, edge_gradients, bool_new):
	black_color = (0, 0, 0)
	pixels = image.load()
	if bool_new:
		image = Image.new("RGB", image.size, "white")
		pixels = image.load()
	for gradient_key in edge_gradients:
		y, x = gradient_key
		pixels[x, y] = black_color
	return image
	
def define_edges(image, mask_to_use, bool_enhance):
	bool_normalize = False
	edge_gradients = find_edges(image, mask_to_use, bool_normalize)
	edge_image = draw_edges(image, edge_gradients, True) #new image
	if bool_enhance:
		enhance_edge_image = pix.enhance_pixels(edge_image, True)
		return enhance_edge_image
	else:
		return edge_image

def __main__(filename, choice_mask, choice_save):
	if choice_mask[0]:
		mask_to_use = choice_mask[1]
	else:
		mask_to_use = "sobeldg" #default
	original_image = Image.open(filename)
	rgb_image = original_image.convert('RGB')
	image = pix.grayscale_image(rgb_image)
	edge_image = define_edges(image, mask_to_use, True)
	edge_image.show()
	if choice_save[0]:
		bool_save =  files.validate_save("edges\output\\", choice_save[1], '.png')
		if bool_save[0]:
			print "Directory of the new image: {}".format(bool_save[1])
			edge_image.save(bool_save[1])
	return None

#run in the 'package' directory
if __name__ == '__main__':
	pre_options = files.validate_arguments(sys.argv)
	__main__(pre_options[0], pre_options[1], pre_options[2])
