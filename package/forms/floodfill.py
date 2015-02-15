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

	#bfs(pixels, x, y, xs, ys, edge_color, background_color, newcolor)
def bfs(image, remplazo, valor, cola, ys, xs, visitados):
	pixels = image.load()
	(y, x) = cola.pop(0)
	#print x, y
	actual = pixels[x, y]
	#print y, x, actual
	#print actual, valor
	#print pixels[x, y]
	#print "hola"
	if valor == pixels[x, y]:
		pixels[x, y] = remplazo
	else:
		return None
	#print pixels[x, y], valor
	#print pixels[x, y]
	for dy in xrange(y - 1, y + 2):
		for dx in xrange(x - 1, x + 2):
			#print dy, dx, ys, xs
			if dy >= 0 and dy < ys:
				if dx >= 0 and dx < xs:
					candidato = (dy, dx)
					if candidato not in visitados:
						contenido = pixels[dx, dy]
						#print contenido
						if contenido == valor:
							cola.append(candidato)
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
					if not color == (255, 0, 0):
						pixels[x, y] = (255, 255, 255)
					else:
						pixels[x, y] = (0, 0, 0)
	return None

def colorear(image, edge_color, background_color):
	xs, ys = image.size
	pixels = image.load()
	color_list = list()
	for y in xrange(0, ys):
		for x in xrange(0, xs):
			pixel = pixels[x, y]
			if pixel == background_color:
				newcolor = rout.new_color()
				color_list.append(newcolor)
				bfs(pixels, x, y, xs, ys, edge_color, background_color, newcolor)
				
	print "total_colore", len(lista_colores)

if __name__ == '__main__':
	#pre_options = aux.pre_argv(sys.argv)
	#__main__(pre_options[0], pre_options[1], pre_options[2])
	filename = "samples\\flood.png"
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
	edge_color, background_color = (0, 0, 0), (255, 255, 25)
	colorear(image, edge_color, background_color)
	image.show()