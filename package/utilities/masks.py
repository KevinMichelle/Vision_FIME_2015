from PIL import Image
import sys
import os.path
import random
import utilities.files as files
import utilities.pix as pix
import utilities.neighbors as neighbors

def mask_info(mask):
	if (type(mask) is tuple) or (type(mask) is list):
		mask_y = len(mask)
	else:
		#Error
		print "Error1"
		quit()
	if (type(mask[0]) is tuple) or (type(mask[0]) is list):
		mask_x = len(mask[0])
	else:
		#Error
		print "Error2"
		quit()
	bool_x = True #Asumir que la longitud x de la mascara es verdadera
	suma = 0
	for i in mask:
		contador = 0
		if (type(i) is tuple) or (type(i) is list):
			for j in i:
				contador += 1
				suma += j
			if contador != mask_x:
				bool_x = False
				break
		else:
			#Error
			print "Error3"
			quit()
	if bool_x:
		return (mask_y, mask_x, suma)
	else:
		#Error
		print "Error4"
		quit()
	return None
		
def open_file_mask(name, directory):
	filename = "{}{}".format(directory, name)
	mask_all = []
	if os.path.isfile(filename):
		with open(filename, 'r') as open_file:
			for line in open_file:
				mask = []
				row_mask = []
				for index in xrange(len(line)):
					if line[index].isdigit():
						row_mask.append(int(line[index]))
						if (index - 1) >= 0:
							if line[index - 1] == "-":
								row_mask[len(row_mask) - 1] *= (-1)
					elif line[index] == "," or line[index] == "\n":
						mask.append(tuple(row_mask))
						row_mask = []
				if len(row_mask) > 0:
					mask.append(tuple(row_mask))
				mask_all.append(mask)
		return mask_all
	else:
		return None
		
#http://stackoverflow.com/a/306417
def define_mask(mask_to_use):
	mask = []
	extension = ".txt"
	if mask_to_use is not None:
		filename = "{}{}".format(mask_to_use, extension)
		directory = "utilities\masks\special\\"
		mask = open_file_mask(filename, directory)
		if mask is None:
			directory = "utilities/masks/special/"
			mask = open_file_mask(filename, directory)
	else:
		directory = "utilities\masks\\"
		file_mask = files.find_files(directory, extension)
		for file in file_mask:
			dummy_mask = open_file_mask(file, directory)
		mask = random.choice(dummy_mask)
	return mask

def mask_pixel_operator(image, mask, bool_normalize):
	xs, ys = image.size
	pixels = image.load()
	mask_y_size, mask_x_size, mask_weight = mask_info(mask)
	mask_values = find_mask_values(mask)
	parameters = mask_y_size, mask_x_size #mask size
	axis_limits = (ys, xs)
	lower_y, upper_y, lower_x, upper_x = neighbors.neighbor_limits(parameters)
	first_y = lower_y
	first_x = lower_x
	last_y = ys - lower_y
	last_x = xs - lower_x
	new_pixels = {}
	for y in xrange(ys):
		for x in xrange(xs):
			pixel = (y, x)
			neighbor_pixels = neighbors.find_neighbors(pixels, pixel, None, axis_limits)
			new_pixel_value = 0
			for index in xrange(len(neighbor_pixels)):
				n_pixel = neighbor_pixels[index][1][0] #pixel value
				n_mask = mask_values[index]
				aux = n_pixel * n_mask
				new_pixel_value += aux
			if pixel not in new_pixels:
				if bool_normalize:
					new_pixels[pixel] = new_pixel_value/mask_weight
				else:
					new_pixels[pixel] = new_pixel_value
	return new_pixels
	
	
def apply_mask(image, mask_to_use, bool_normalize):
	mask = define_mask(mask_to_use)
	if mask is None:
		print "Not define mask"
		quit()
	else:
		if __name__ == '__main__':
			print "Mask to use", mask
	new_pixels = mask_pixel_operator(image, mask, bool_normalize)
	return new_pixels
	
def find_mask_values(mask):
	mask_values = []
	for y in mask:
		for x in y:
			mask_values.append(x)
	return mask_values
	
def __main__(filename, choice_mask, choice_save):
	if choice_mask[0]:
		mask_to_use = choice_mask[1]
	else:
		mask_to_use = None
	original_image = Image.open(filename)
	rgb_image = original_image.convert('RGB')
	image = pix.grayscale_image(rgb_image)
	bool_normalize = True
	new_pixels = apply_mask(image, mask_to_use, bool_normalize)
	new_image = pix.change_pixels(image, new_pixels)
	image.show()
	new_image.show()
	if choice_save[0]:
		bool_save =  files.validate_save("samples\destination\\", choice_save[1], '.png')
		if bool_save[0]:
			print "Directory of the new image: {}".format(bool_save[1])
			new_image.save(bool_save[1])
	#new_image.show()
	return None

#run in the 'package' directory
if __name__ == '__main__':
	pre_options = files.validate_arguments(sys.argv)
	__main__(pre_options[0], pre_options[1], pre_options[2])
