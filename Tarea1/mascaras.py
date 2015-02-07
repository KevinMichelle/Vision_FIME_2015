from PIL import Image
import ImageDraw
import sys
import os.path
import math

mascara1 = [(1, 4, 1), (4, 8, 4), (1, 4, 1)]
mascara2 = [(1, 2, 1), (2, 4, 2), (1, 2, 1)]

def info_mascara(mascara):
	if (type(mascara) is tuple) or (type(mascara) is list):
		y_masc = len(mascara)
	else:
		#Error
		quit()
	if (type(mascara[0]) is tuple) or (type(mascara[0]) is list):
		x_masc_prob = len(mascara[0])
	else:
		#Error
		quit()
	bool_x = True #Asumir que la longitud x de la mascara es verdadera
	suma = 0
	for i in mascara:
		contador = 0
		if (type(i) is tuple) or (type(i) is list):
			for j in i:
				contador += 1
				suma += j
			if contador != x_masc_prob:
				bool_x = False
				break
		else:
			#Error
			quit()
	if bool_x:
		return (x_masc_prob, y_masc, suma)
	else:
		#Error
		quit()



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
	
def aplicar_filtro(imagen, opciones):
	tipo_vecinos = opciones[0]
	tipo_filtro = opciones[1]
	xs, ys = imagen.size
	pixeles = imagen.load()
	nueva_imagen = imagen.copy()
	print "Tipo de vecinos: {}, tipo de filtro: {}".format(tipo_vecinos,tipo_filtro)
	pixeles_nuevos = nueva_imagen.load()
	for y in xrange(ys):
		for x in xrange(xs):
			colores_vecinos = encontrar_vecinos(pixeles, x, y)
			rojo_vecinos = colores_vecinos[0]
			verde_vecinos = colores_vecinos[1]
			azul_vecinos = colores_vecinos[2]
			if tipo_filtro == 0:
				# Tipo de filtro: mediana
				rgb = (mediana(rojo_vecinos), mediana(verde_vecinos), mediana(azul_vecinos))
			elif tipo_filtro == 1:
				# Tipo de filtro: promedio aritmetico
				rgb = (promedio(rojo_vecinos), promedio(verde_vecinos), promedio(azul_vecinos))
			pixeles_nuevos[x, y] = rgb
	nueva_imagen.show()
	
def aplicar_mascara(imagen, mascara):
	xs, ys = imagen.size
	pixeles = imagen.load()
	nueva_imagen = imagen.copy()
	pixeles_nuevos = nueva_imagen.load()
	x_masc, y_masc, suma_mascara = info_mascara(mascara)
	iy, sy, ix, sx = ((y_masc-1)/2), ((y_masc+2)/2), ((x_masc-1)/2), ((x_masc+2)/2)
	dummy = 0
	fy, fx, ly, lx= (0 + iy, 0 + ix, ys - iy, xs - ix)
	print (fy, fx), (ly, lx)
	for y in xrange(fy, ly):
		for x in xrange(fx, lx):
			col_masc = 0
			print "y:{}, x:{}, pixel:{}".format(y, x, pixeles[x, y]) 
			for dy in xrange(y - iy, y + sy):
				if dy >= 0 and dy < ys:
					for dx in xrange(x - ix, x + sx):
						fila_masc = 0
						if dx >= 0 and dx < xs:
							dummy += 1
							print "dy:{}, dx:{}".format(dy, dx) 
							#print "dy, dx", dy, dx
							fila_masc += 1
			col_masc += 1
	return None
					

#El pixel se accede con los valores de x, y
def encontrar_vecinos(imagen, x_pixel, y_pixel):
	pixeles = imagen.load()
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
	return (rojo_vecinos, verde_vecinos, azul_vecinos)

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
		
def promedio(lista):
	suma = 0
	for i in lista:
		suma += i
	prom = float(suma) / float(len(lista))
	return int(math.ceil(prom))
	
def main(filename):
	imagen_original = Image.open(filename)
	imagen = imagen_original.convert('L')
	aplicar_mascara(imagen, mascara2)
	

if len(sys.argv) == 2:
	filename = sys.argv[1]
	if os.path.isfile(filename):
		main(filename)
	else:
		print "No existe el archivo %s" %filename
else:
	print 'Numero de entradas incorrecto'
