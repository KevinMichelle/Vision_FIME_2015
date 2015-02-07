from PIL import Image
import sys
import os.path
import math
import rutinas
import procesamiento

mascara1 = [(1, 4, 1), (4, 8, 4), (1, 4, 1)]
mascara2 = [(1, 2, 1), (2, 4, 2), (1, 2, 1)]
sobel = ([(-1, 0, 1), (-2, 0, 2), (-1, 0, 1)], [(1, 2, 1), (0, 0, 0), (-1, -2, -1)])

def mask_info(mask):
	if (type(mask) is tuple) or (type(mask) is list):
		mask_y = len(mask)
	else:
		#Error
		quit()
	if (type(mask[0]) is tuple) or (type(mask[0]) is list):
		mask_x = len(mask[0])
	else:
		#Error
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
			quit()
	if bool_x:
		return (mask_y, mask_x, suma)
	else:
		#Error
		quit()



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
				if new_value > 255:
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
		gradient_mean = rutinas.mediana(gradients_list)
		print gradient_mean
		print rutinas.promedio(gradients_list)
	return new_image
	
def __main__(filename):
	imagen_original = Image.open(filename)
	imagen_original = imagen_original.convert('RGB')
	imagen_grises = procesamiento.escala_grises(imagen_original)
	mascara = sobel
	imagen_mascara = aplicar_mascara(imagen_grises, mascara, True)
	imagen_grises.show()
	imagen_mascara.show()
	
if __name__ == '__main__':
	existe = rutinas.existe_archivo(sys.argv)
	if existe:
		__main__(sys.argv[len(sys.argv) - 1])
