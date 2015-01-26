from PIL import Image
import ImageDraw
import sys
import os.path
import operator
from time import sleep

def encontrar_colores(imagen):
	colores = {}
	w, h = imagen.size
	pixeles = imagen.load()
	for x in xrange(w):
		for y in xrange(h):
			valor_pixel = pixeles[x, y]
			if valor_pixel not in colores:
				colores[valor_pixel] = 1
			else:
				colores[valor_pixel] += 1
	return colores

def prueba_colores(imagen):
	w, h = imagen.size
	pixeles = imagen.load()
	for x in xrange(w):
		for y in xrange(h):
			if (x == 0 and y == 0) or (x == 0 and y == h - 1) or (x == w - 1 and y == 0) or (x == w - 1 and y == h - 1):
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

if len(sys.argv) == 2:
	filename = sys.argv[1]
	if os.path.isfile(filename):
		#imagen = Image.open(filename)
		imagen = Image.new('RGB', (10, 20))
		draw = ImageDraw.Draw(imagen)
		imagen_datos = imagen.getdata()
		hola1 = encontrar_colores(imagen)
		print hola1
		hola2 = encontrar_colores(imagen)
		print hola2
		prueba_colores(imagen)
	else:
		print "No existe el archivo %s" %filename
else:
	print 'Numero de entradas incorrecto'
