from PIL import Image
import sys
import os.path
import math
import random
import routines.routines as rout
import routines.auxiliary as aux


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
		
def open_file_mask(file, dir):
	file_name_list = []
	file_name_list.append(dir)
	file_name_list.append(file)
	file_name = "".join(file_name_list)
	mask_all = []
	if os.path.isfile(file_name):
		with open(file_name, 'r') as open_file:
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
		
def define_mask(options):
	mask = []
	ext = ".txt"
	if options[0]:
		name = options[1]
		file_list = []
		file_list.append(name)
		file_list.append(ext)
		file = "".join(file_list)
		dir = "edge_detection\masks\special\\"
		mask = open_file_mask(file, dir)
	else:
		dir = "edge_detection\masks\\"
		file_mask = aux.traer_archivos(dir, ext)
		for file in file_mask:
			dummy_mask = open_file_mask(file, dir)
		mask = random.choice(dummy_mask)
	return mask
	
	
def aplicar_mascara(image, mask, multiple):
	if mask is None:
		print "Not defined mask"
		quit()
	else:
		print "Mask to use", mask
	if multiple:
		pixel_gradient = []
		gradients = {}
		mask1 = mask[0]
		mask2 = mask[1]
		mask1_info = mask_info(mask1)
		mask2_info = mask_info(mask2)
		if mask1_info == mask2_info:
			mask_y_size, mask_x_size, mask_weight = mask1_info
	else:
		mask_y_size, mask_x_size, mask_weight = mask_info(mask)

	#datos de la imagen
	xs, ys = image.size
	pixels = image.load()
	new_image = image.copy()
	new_pixels = new_image.load()
	
	#definir limites
	lower_y = ( (mask_y_size - 1) / 2)
	upper_y = ( (mask_y_size + 2) / 2)
	lower_x = ( (mask_x_size - 1) / 2)
	upper_x = ( (mask_x_size + 2) / 2)
	
	#definir posiciones
	first_y = lower_y
	first_x = lower_x
	last_y = ys - lower_y
	last_x = xs - lower_x

	
	for y in xrange(first_y, last_y):
		for x in xrange(first_x, last_x):
			column_mask = 0
			if multiple:
				sumatoria1 = 0
				sumatoria2 = 0
			else:
				sumatoria = 0
			for dy in xrange(y - lower_y, y + upper_y):
				if dy >= 0 and dy < ys:
					row_mask = 0
					for dx in xrange(x - lower_x, x + upper_x):
						if dx >= 0 and dx < xs:
							if multiple:
								sumatoria1 += pixels[dx, dy][0] * mask1[column_mask][row_mask]
								sumatoria2 += pixels[dx, dy][0] * mask2[column_mask][row_mask]
								#print sumatoria1, dy, dx
							else:
								sumatoria += pixels[dx, dy][0] * mask[column_mask][row_mask]
							row_mask += 1
				column_mask += 1
			new_value = 0
			if not multiple:
				new_value = sumatoria / mask_weight
				new_pixels[x, y] = (new_value, new_value, new_value)
			else:
				pixel = pixels[x, y]
				#new_pixels[x, y] = (pixel[0], pixel[1], pixel[2])
				new_pixels[x, y] = (255, 255, 255)
				new_value = int(math.pow(abs(sumatoria1) + abs(sumatoria2), 2))
				if new_value not in gradients:
					gradients[new_value] = 1
				else:
					gradients[new_value] += 1
				pixel_gradient.append((x, y, new_value))
	if multiple:
		new_pixel_gradient = edge_detection(gradients, pixel_gradient)
		for index_pixel in xrange(0, len(new_pixel_gradient)):
			new_pixel_info = new_pixel_gradient[index_pixel]
			nxp, nyp, nvp = new_pixel_info[0], new_pixel_info[1], new_pixel_info[2]
			if nvp == 1:
				new_pixels[nxp, nyp] = (0, 0, 0)
	return new_image
	
def edge_detection(gradients, pixel_gradient):
	new_pixel_gradient = []
	gradients_list = aux.dict_to_list(gradients, False)
	threshold = aux.promedio(gradients_list) #dummy value
	for index_pixel in xrange(0, len(pixel_gradient)):
		pixel_info = pixel_gradient[index_pixel]
		if pixel_info[2] >= threshold:
			new_pixel_gradient.append((pixel_info[0], pixel_info[1], 1))
	return new_pixel_gradient
	
def __main__(filename, choice_mask, choice_save):
	options_mask = []
	multiple_mask = False
	print filename
	if choice_mask[0]:
		mask_to_use = choice_mask[1]
		multiple_mask = True
		options_mask.append(True)
		options_mask.append(mask_to_use)
	else:
		options_mask = [False, None]
	mask = define_mask (options_mask)
	imagen_original = Image.open(filename)
	imagen_original = imagen_original.convert('RGB')
	imagen_grises = rout.escala_grises(imagen_original)
	new_image = aplicar_mascara(imagen_grises, mask, multiple_mask)
	if choice_save[0]:
		bool_save =  aux.checar_guardar("dest\\", choice_save[1], '.png')
		if bool_save[0]:
			print "Directory of the new image: {}".format(bool_save[1])
			new_image.save(bool_save[1])
	new_image.show()
	return None

#run in the 'package' directory
#python -m edge_detection.mascaras ejemplos\shantae.png
if __name__ == '__main__':
	pre_options = aux.pre_argv(sys.argv)
	__main__(pre_options[0], pre_options[1], pre_options[2])
