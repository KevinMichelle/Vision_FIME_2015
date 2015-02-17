from PIL import Image
import sys
import os.path
import math
import random
import colorsys
import routines.routines as rout
import routines.auxiliary as aux

def check_colors(image):
	xs, ys = image.size
	pixels = image.load()
	dict_colors = {}
	for y in xrange(ys):
		if y >= 0 and y < ys:
			for x in xrange(xs):
				if x >= 0 and x < xs:
					pixel_value = pixels[x, y]
					if pixel_value not in dict_colors:
						dict_colors[pixel_value] = 1
					else:
						dict_colors[pixel_value] += 1
	colors = aux.dict_to_list_tuple(dict_colors)
	return colors
	
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
		
def main():
	return None
	
def change_color(image, oldcolor, newcolor):
	print "old, new", oldcolor, newcolor
	pixels = image.load()
	xs, ys = image.size
	for y in xrange(ys):
		for x in xrange(xs):
			if y >= 0 and y < ys:
				if x >= 0 and x < xs:
					color = pixels[x, y]
					if oldcolor is None and newcolor is None:
						if not color == (0, 0, 0):
							pixels[x, y] = (255, 255, 255)
					else:
						if color == oldcolor:
							pixels[x, y] = newcolor
	return None

def enhance_edge(image, bool_edges):
	y_neighbors, x_neighbors = 5, 5
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
	change_color(image, None, None) #remove pixels that are not white or black
	image = enhance_edge(image, True) #se crea un nuevo objeto tipo Image, ya es distinto que el que recibe flood_fill
	image.show()
	white_color, black_color = (255, 255, 255), (0, 0, 0)
	xs, ys = image.size
	pixels = image.load()
	color_list = list()
	max_color_count = 0
	background_new_color = ()
	center_mass = {} #color -> center of mass
	for y in xrange(0, ys):
		for x in xrange(0, xs):
			pixel = pixels[x, y]
			if pixel == white_color:
				visitados = {}
				newcolor = rout.gen_color(color_list)
				color_list.append(newcolor)#generador de colores llamada incompleto
				queue_neighbors = list()
				queue_neighbors.append((y, x))
				while len(queue_neighbors) > 0:
					bfs(image, queue_neighbors, white_color, newcolor, visitados)
				if len(visitados) > max_color_count:
					background_new_color = newcolor
					max_color_count = len(visitados)
				if len(visitados) > 0:
					new_center_mass = center_of_mass(image, visitados)
					center_mass[newcolor] = new_center_mass
	print "centro_masas", center_mass
	if background_new_color in center_mass:
		del center_mass[background_new_color]
	print "centro_masas", center_mass
	change_color(image, background_new_color, white_color) #replace the new back ground color with the white color
	change_color(image, black_color, white_color)
	draw_center_mass(image, center_mass)
	return image
	
def draw_center_mass(image, center_mass):
	black_color = (0, 0, 0)
	xs, ys = image.size
	pixels = image.load()
	for color in center_mass:
		center = center_mass[color]
		y, x = center[0], center[1]
		for dy in xrange(y - 3, y + 4):
			if dy >= 0 and dy < ys:
				for dx in xrange(x - 3, x + 4):
					if dx >= 0 and dx < xs:
						pixels[dx, dy] = black_color
	return None
	
def edge_dictio(image):
	edge_color = (0, 0, 0)
	xs, ys = image.size
	pixels = image.load()
	id = 0
	edge_pixels = {}
	edge_id = {}
	for y in xrange(ys):
		for x in xrange(xs):
			pixel = pixels[x, y]
			if pixel == edge_color:
				if (y, x) not in edge_pixels:
					id += 1
					visitados = {}
					queue_neighbors = [(y, x)]
					while len(queue_neighbors) > 0:
						bfs(image, queue_neighbors, edge_color, edge_color, visitados)
					visitados_lista = aux.dict_to_list(visitados, True) #only the keys
					for element in visitados_lista:
						edge_pixels[element] = id
					edge_id[id] = visitados_lista
	return edge_id
	
def jarvis(image):
	pixels = image.load()
	edge_id = edge_dictio(image)
	for id in edge_id:
		y, x = [], []
		edge_points = edge_id[id]
		for points in edge_points:
			y.append(points[0])
		y.sort()
		lower_y = y[len(y)-1]
		for points in edge_points:
			if points[0] == lower_y:
				x.append(points[1])
		x.sort()
		upper_x = x[len(x)-1]
		print "y, x", (lower_y, upper_x)
	return None

if __name__ == '__main__':
	#pre_options = aux.pre_argv(sys.argv)
	#__main__(pre_options[0], pre_options[1], pre_options[2])
	filename = "samples\\circulos.png"
	print filename
	original_image = Image.open(filename)
	image = original_image.convert('RGB')
	pixels = image.load()
	colors = check_colors(image)
	colors_sort = aux.sort_tuple(colors)
	print colors_sort
	#print "hola"
	#print colors_sort
	xs, ys = image.size
	#print cola
	valor = (255, 255, 255)
	#print "hola"
	#print colors_sort
	visitados = {}
	counter = 0
	colores = []
	while counter < len(colores):
		cola = []
		remplazo = colores[counter%len(colores)]
		y_random = random.randint(0, ys - 1)
		x_random = random.randint(0, xs - 1)
		cola.append((y_random, x_random))
		#while len(cola) > 0:
		#	bfs(image, remplazo, valor, cola, ys, xs, visitados)
		#counter += 1
		break
	colors = check_colors(image)
	image = flood_fill(image)
	image.show()
	image.save('formas.png')
	jarvis(image)