from PIL import Image
import sys
import os.path
import math
import random
import routines.routines as routines
import routines.auxiliary as auxiliary


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
				for element in line:
					if element.isdigit():
						row_mask.append(int(element))
					elif element == "," or element == "\n":
						mask.append(tuple(row_mask))
						row_mask = []
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
		file = []
		file_list.append(name)
		file_list.append(ext)
		file = "".join(file_list)
		dir = "edge_detection\masks\special\\"
		mask = open_file_mask(file, dir)
	else:
		dir = "edge_detection\masks\\"
		file_mask = auxiliary.traer_archivos(dir, ext)
		for file in file_mask:
			dummy_mask = open_file_mask(file, dir)
		mask = random.choice(dummy_mask)
	return mask
		



def prueba_colores(imagen):
	xs, ys = imagen.size
	pixeles = imagen.load()
	for y in xrange(ys):
		for x in xrange(xs):
			if (y == 0 and x == 0) or (y == 0 and x == xs - 1) or (y == ys - 1 and x == 0) or (y == ys - 1 and x == xs - 1):
				if (x == 0 and y == 0):
					pixeles[x, y]  = (255, 0, 0)
				elif (x == 0 and y == ys - 1):
					pixeles[x, y]  = (0, 255, 0)
				elif (x == xs - 1 and y == 0):
					pixeles[x, y]  = (0, 0, 255)
				elif (x == xs - 1 and y == ys - 1):
					pixeles[x, y] = (255, 255, 255)
	
	
def aplicar_mascara(image, mask, multiple):
	if mask == 2:
		mask_
	dummy = 0
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
				new_value = abs(sumatoria1) + abs(sumatoria2)
				if new_value not in gradients:
					gradients[new_value] = 1
				else:
					gradients[new_value] += 1
				pixel_gradient.append((y, x, new_value))
				if new_value > 200:
					new_pixels[x, y] = (0, 0, 255)
				else:
					new_pixels[x, y] = (255, 255, 255)
	if multiple:
		for i in gradients:
			print i
		print gradients
		gradients_list = []
		for i in gradients:
			gradients_list.append(i)
		gradient_mean = auxiliary.mediana(gradients_list)
		print gradient_mean
		print auxiliary.promedio(gradients_list)
	return new_image
	
def __main__(filename, bool_mask):
	options_mask = []
	if bool_mask:
		mask_to_use = sys.argv[2]
		options_mask.append(True)
		options_mask.append(mask_to_use)
	else:
		options_mask.append(False)
	mask = define_mask (options_mask)
	imagen_original = Image.open(filename)
	imagen_original = imagen_original.convert('RGB')
	imagen_grises = routines.escala_grises(imagen_original)
	imagen_mascara = aplicar_mascara(imagen_grises, mask, bool_mask)
	imagen_grises.show()
	imagen_mascara.show()

#run in the 'package' directory
#python -m edge_detection.mascaras ejemplos\shantae.png
if __name__ == '__main__':
	existe = auxiliary.existe_archivo(sys.argv)
	if existe:
		bool_mask = False
		if len(sys.argv) > 2:
			if sys.argv[1] == "-m" or sys.argv[1] == "m" or sys.argv[1] == "-M" or sys.argv[1] == "M":
				bool_mask = True
		__main__(sys.argv[len(sys.argv) - 1], bool_mask)
