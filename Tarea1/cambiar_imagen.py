from PIL import Image
import ImageDraw
import sys
import os.path
import operator
import math
import datetime

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
	
def aplicar_filtro(imagen):
	inicio = datetime.datetime.now()
	xs, ys = imagen.size
	pixeles = imagen.load()
	nueva_imagen = imagen.copy()
	pixeles_a_filtrar = nueva_imagen.load()
	for y in xrange(ys):
		for x in xrange(xs):
			rgb = encontrar_vecinos(pixeles, x, y)
			pixeles_a_filtrar[x, y] = rgb
	imagen.show()
	nueva_imagen.show()
	fin = datetime.datetime.now()
	tiempo_ejecucion = fin - inicio
	print "\tTiempo para modificar la imagen {} : {} segundos".format((xs, ys), tiempo_ejecucion)

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
					pixel = pixeles[x, y]
					rojo_vecinos.append(pixel[0])
					verde_vecinos.append(pixel[1])
					azul_vecinos.append(pixel[2])
	rojo_vecinos.sort()
	verde_vecinos.sort()
	azul_vecinos.sort()
	return (mediana(rojo_vecinos), mediana(verde_vecinos), mediana(azul_vecinos))

#Implementacion basada en la descripcion de Wikipedia y la respuesta de Stack Overflow
#http://en.wikipedia.org/wiki/Median#Medians_for_samples
#http://stackoverflow.com/questions/24101524/finding-median-of-list-in-python/24101655#24101655
#Nota_Las listas empiezan en la posicion 0, por eso asi es el algoritmo
def mediana(lista):
	if len(lista) % 2 == 0:
		suma = lista[(len(lista) / 2) - 1] + lista[len(lista)/2]
		mediana_par =  math.ceil(suma / 2.0)
		return int(mediana_par)
	else:
		return lista[((len(lista) + 1)/2) - 1]
	

if len(sys.argv) == 2:
	filename = sys.argv[1]
	if os.path.isfile(filename):
		imagen_original = Image.open(filename)
		imagen = imagen_original.convert('RGB')
		#imagen = Image.new('RGB', (5, 5))
		draw = ImageDraw.Draw(imagen)
		imagen_datos = imagen.getdata()
		aplicar_filtro(imagen)
		prueba_colores(imagen)
	else:
		print "No existe el archivo %s" %filename
else:
	print 'Numero de entradas incorrecto'
