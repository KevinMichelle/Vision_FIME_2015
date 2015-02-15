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

def bfs(image, queue_neighbors, edge_color, background_color, newcolor):
	pixels = image.load()
	y, x = queue_neighbors.pop(0)
	actual_pixel = pixels[x, y]
	pixels[x, y] = newcolor
	for dy in xrange(y - 1, y + 2):
		for dx in xrange(x - 1, x + 2):
			if ((dy == y - 1) and (dx == x)) or ((dy == y) and (dx == x - 1)) or ((dy == y) and (dx == x + 1)) or ((dy == y + 1) and (dx == x)):
				if dy >= 0 and dy < ys:
					if dx >= 0 and dx < xs:
						candidato = (dy, dx)
						if candidato not in visitados:
							contenido = pixels[dx, dy]
							if contenido == background_color:
								queue_neighbors.append(candidato)
								visitados[candidato] = 1
	return None

def main():
	return None
	
def cambiar_colores(image):
	pixels = image.load()
	xs, ys = image.size
	#print ys, xs
	for y in xrange(ys):
		for x in xrange(xs):
			if y >= 0 and y < ys:
				if x >= 0 and x < xs:
					color = pixels[x, y]
					if not color == (0, 0, 0):
						pixels[x, y] = (255, 255, 255)
					else:
						pixels[x, y] = (0, 0, 0)
	return None

def colorear(image, edge_color, background_color):
	xs, ys = image.size
	pixels = image.load()
	color_list = list()
	visitados = {}
	print edge_color, background_color
	for y in xrange(0, ys):
		for x in xrange(0, xs):
			pixel = pixels[x, y]
			if pixel == background_color:
				newcolor = rout.new_color()
				color_list.append(newcolor)
				print newcolor
				queue_neighbors = list()
				queue_neighbors.append((y, x))
				while len(queue_neighbors) > 0:
					bfs(image, queue_neighbors, edge_color, background_color, newcolor)
	print "total_colore", len(color_list), color_list

if __name__ == '__main__':
	#pre_options = aux.pre_argv(sys.argv)
	#__main__(pre_options[0], pre_options[1], pre_options[2])
	filename = "samples\\figuras.png"
	print filename
	original_image = Image.open(filename)
	image = original_image.convert('RGB')
	pixels = image.load()
	cambiar_colores(image)
	#print "hola"
	#print colors_sort
	xs, ys = image.size
	#print cola
	valor = (255, 255, 255)
	#print "hola"
	#print colors_sort
	visitados = {}
	image.show()
	colors = check_colors(image)
	colors_sort = aux.sort_tuple(colors)
	print colors_sort
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
	edge_color, background_color = (0, 0, 0), (255, 255, 255)
	colorear(image, edge_color, background_color)
	image.show()