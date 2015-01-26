from PIL import Image
import ImageDraw
import sys
import os.path
import operator


#Si, lo recorro de manera diferente que en otras funciones
def encontrar_colores(imagen):
	colores = {}
	xs, ys = imagen.size
	pixeles = imagen.load()
	for x in xrange(xs):
		for y in xrange(ys):
			valor_pixel = pixeles[x, y]
			if valor_pixel not in colores:
				colores[valor_pixel] = 1
			else:
				colores[valor_pixel] += 1
	return colores

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
				print x, y, pixeles[x, y]
	
def aplicar_filtro(imagen):
	xs, ys = imagen.size
	pixeles = imagen.load()
	for y in xrange(ys):
		for x in xrange(xs):
			print "muestra1", y, x, pixeles[x, y]
			encontrar_vecinos(pixeles, x, y)

#El pixel se accede con los valores de x, y
def encontrar_vecinos(pixeles, x_pixel, y_pixel):
	xs, ys = imagen.size
	rojo_vecinos = []
	verde_vecinos = []
	azul_vecinos = []
	for y in xrange(y_pixel - 1, y_pixel + 2):
		if y >= 0 and y < ys:
			for x in xrange(x_pixel - 1, x_pixel + 2):
				if x >= 0 and x < xs:
					print y, x
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
		print "hola"
		print imagen.size
	else:
		print "No existe el archivo %s" %filename
else:
	print 'Numero de entradas incorrecto'
