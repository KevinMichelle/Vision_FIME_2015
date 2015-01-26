from PIL import Image
import ImageDraw
import sys
import os.path
import operator

def encontrar_colores(imagen):
	colores = {}
	w, h = imagen.size
	pixeles = imagen.load()
	for y in xrange(h):
		for x in xrange(w):
			valor_pixel = pixeles[x, y]
			if valor_pixel not in colores:
				colores[valor_pixel] = 1
			else:
				colores[valor_pixel] += 1
	return colores

def prueba_colores(imagen):
	w, h = imagen.size
	pixeles = imagen.load()
	for y in xrange(h):
		for x in xrange(w):
			if (y == 0 and x == 0) or (y == 0 and x == w - 1) or (y == h - 1 and x == 0) or (y == h - 1 and x == w - 1):
				if (x == 0 and y == 0):
					pixeles[x, y]  = (255, 0, 0)
				elif (x == 0 and y == h - 1):
					pixeles[x, y]  = (0, 255, 0)
				elif (x == w - 1 and y == 0):
					pixeles[x, y]  = (0, 0, 255)
				elif (x == w - 1 and y == h - 1):
					pixeles[x, y] = (255, 255, 255)
				print x, y, pixeles[x, y]
	imagen.show()
	
def aplicar_filtro(imagen):
	w, h = imagen.size
	pixeles = imagen.load()
	for y in xrange(h):
		for x in xrange(w):
			print x, y, pixeles[x, y]
			encontrar_vecinos(imagen, x, y)

def encontrar_vecinos(imagen, x_pixel, y_pixel):
	rojo_vecinos = []
	verde_vecinos = []
	azul_vecinos = []
	pixeles = imagen.load()
	w, h = imagen.size
	for y in xrange(y_pixel - 1, y_pixel + 2):
		if y >= 0 and y < h:
			for x in xrange(x_pixel - 1, x_pixel + 2):
				print "x", x
				if x >= 0 and x < w:
					pixel = pixeles[x, y]
					rojo_vecinos.append(pixel[0])
					verde_vecinos.append(pixel[1])
					azul_vecinos.append(pixel[2])
	print
	print "rojos", rojo_vecinos
	print "verde", verde_vecinos
	print "azul", azul_vecinos
	print

if len(sys.argv) == 2:
	filename = sys.argv[1]
	if os.path.isfile(filename):
		imagen = Image.open(filename)
		#imagen = Image.new('RGB', (5, 5))
		draw = ImageDraw.Draw(imagen)
		imagen_datos = imagen.getdata()
		aplicar_filtro(imagen)
		prueba_colores(imagen)
	else:
		print "No existe el archivo %s" %filename
else:
	print 'Numero de entradas incorrecto'
