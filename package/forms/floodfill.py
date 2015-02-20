from PIL import Image, ImageDraw
import sys
import os.path
import math
import random
import colorsys
import routines.routines as rout
import routines.auxiliary as aux
import edge_detection.mascaras as masc
	
#http://stackoverflow.com/a/22620206
def center_of_mass(image, list_of_pixels):
	sum_y, sum_x = 0, 0
	len_pixels = len(list_of_pixels)
	for pixel in list_of_pixels:
		sum_y += pixel[0]
		sum_x += pixel[1]
	return (sum_y/len_pixels, sum_x/len_pixels)

def bfs(image, queue_neighbors, background_color, newcolor, visitados): #checar nombre
	pixels = image.load()
	xs, ys = image.size
	y, x = queue_neighbors.pop(0)
	pixels[x, y] = newcolor
	for dy in xrange(y - 1, y + 2):
		for dx in xrange(x - 1, x + 2):
			if dy >= 0 and dy < ys:
				if dx >= 0 and dx < xs:
					if ((dy == y - 1) and (dx == x)) or ((dy == y) and (dx == x - 1)) or ((dy == y) and (dx == x + 1)) or ((dy == y + 1) and (dx == x)):
						candidato = (dy, dx)
						if candidato not in visitados:
							contenido = pixels[dx, dy]
							if contenido == background_color:
								queue_neighbors.append(candidato)
								visitados[candidato] = 1
	return None
	
def enhance_edge(image, bool_edges):
	y_neighbors, x_neighbors = 7, 7
	if bool_edges: # para rellenar bordes
		control = 3
	else: # para suavizar bordes
		control = 9
	pixels = image.load()
	xs, ys = image.size
	new_image = image.copy()
	new_pixels = new_image.load()
	for y in xrange(ys):
		for x in xrange(xs):
			count = 0 #neighbor where their value is (0, 0, 0) -> edges
			neighbors = rout.find_neighbors(pixels, y, x, x_neighbors, x_neighbors, ys, xs)
			for pixel in neighbors:
				if pixel == (0, 0, 0):
					count += 1
			if bool_edges:
				if count > control:
					new_pixels[x, y] = (0, 0, 0)
			else:
				if count >=control:
					new_pixels[x, y] = (255, 255, 255) #para borrar luego
	return new_image

def flood_fill(image):
	rout.change_color(image, None, None) #remove pixels that are not white or black
	image = enhance_edge(image, True) #se crea un nuevo objeto tipo Image, ya es distinto que el que recibe flood_fill
	white_color, black_color = (255, 255, 255), (0, 0, 0)
	xs, ys = image.size
	pixels = image.load()
	color_list = list()
	max_color_count = 0
	background_new_color = ()
	info_form = {}
	for y in xrange(0, ys):
		for x in xrange(0, xs):
			pixel = pixels[x, y]
			if pixel == white_color:
				visitados = {}
				newcolor = rout.gen_color(color_list)
				color_list.append(newcolor)#generador de colores llamada incompleto
				visitados[(y, x)] = 1
				queue_neighbors = list()
				queue_neighbors.append((y, x))
				while len(queue_neighbors) > 0:
					bfs(image, queue_neighbors, white_color, newcolor, visitados)
				if len(visitados) > max_color_count:
					background_new_color = newcolor
					max_color_count = len(visitados)
				if len(visitados) > 0:
					new_center_mass = center_of_mass(image, visitados)
					info = find_info_form(visitados)
					info_form[newcolor] = (info, new_center_mass, len(visitados), newcolor)
	if background_new_color in info_form:
		del info_form[background_new_color]
	rout.change_color(image, background_new_color, white_color) #replace the new back ground color with the white color
	rout.change_color(image, black_color, white_color)
	#draw_center_mass(image, center_mass)
	draw_info_form(image, info_form)
	return image
	
def draw_center_mass(image, center):
	black_color = (0, 0, 0)
	xs, ys = image.size
	pixels = image.load()
	y, x = center[0], center[1]
	for dy in xrange(y - 3, y + 4):
		if dy >= 0 and dy < ys:
			for dx in xrange(x - 3, x + 4):
				if dx >= 0 and dx < xs:
					pixels[dx, dy] = black_color
	return None
	
#http://effbot.org/imagingbook/imagedraw.htm
def draw_info_form(image, info_form):
	black_color = (0, 0, 0)
	pixels = image.load()
	xs, ys = image.size
	total = xs * ys
	for llave in info_form:
		info = info_form[llave]
		form = info[0]
		center_mass = info[1]
		size_form = info[2]
		color_form = info[3]
		porcentaje = round((float(size_form) * 100.0) / float(total), 2)
		texto = "{} %".format(porcentaje)
		y1, y2 = form[0]
		x1, x2 = form[1]
		pix1, pix2, pix3, pix4 = (x1, y1), (x1, y2), (x2, y1), (x2, y2)
		draw = ImageDraw.Draw(image)
		draw.line((pix1, pix3), fill = black_color)
		draw.line((pix1, pix2), fill = black_color)
		draw.line((pix4, pix2), fill = black_color)
		draw.line((pix4, pix3), fill = black_color)
		draw_center_mass(image, center_mass)
		center_y, center_x = center_mass[0], center_mass[1]
		draw.text((center_x, center_y + 10), texto, fill=black_color)
		print "Figura con color {}, centro de masa en {}, porcentaje que ocupa en la imagen {}".format(color_form, center_mass, porcentaje)
	return None


	
def find_info_form(list_of_pixels):
	y, x = [], []
	for pixel in list_of_pixels:
		y.append(pixel[0])
		x.append(pixel[1])
	y.sort()
	x.sort()
	y_ = (y[0], y[len(y) - 1])
	x_ = (x[0], x[len(x) - 1])
	return (y_, x_)
	
def __main__(filename, choice_edge, choice_save):
	choice_edge = None #dummy value for the moment
	original_image = Image.open(filename)
	original_image = original_image.convert('RGB')
	image = rout.escala_grises(original_image)
	options_mask = (True, "prewittdg")
	mask = masc.define_mask(options_mask)
	multiple_mask = True
	edge_image = masc.apply_mask(image, mask, multiple_mask) #change name
	new_image = flood_fill(edge_image)
	new_image.show()
	if choice_save[0]:
		bool_save =  aux.checar_guardar("dest\\", choice_save[1], '.png')
		if bool_save[0]:
			print "Directory of the new image: {}".format(bool_save[1])
			new_image.save(bool_save[1])
	return None
	
if __name__ == '__main__':
	pre_options = aux.pre_argv(sys.argv)
	__main__(pre_options[0], pre_options[1], pre_options[2])