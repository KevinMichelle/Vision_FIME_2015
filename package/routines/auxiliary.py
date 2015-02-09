import os
import math
import numpy as np
import matplotlib.pyplot as plt

def preparar_nombre(nombre):
	bool_nombre = True
	for letra in nombre:
		valor = ord(letra)
		if not (valor >= 48 and valor <= 57):
			if not(valor >= 65 and valor <= 90):
				if not (valor >= 97 and valor <= 122):
					bool_nombre = False
					return bool_nombre
	return bool_nombre

def dict_to_list(dictio):
	new_list = []
	for element in dictio:
		count = dictio[element]
		for dummy in xrange(0, count):
			new_list.append(element)
	return new_list
			

def histogram(info):
	if type(info) is dict:
		data = dict_to_list(info)
	elif type(info) is list:
		data = info
	bin_width = 1
	plt.hist(data, bins=np.arange(min(data), max(data) + bin_width, bin_width))
	plt.show()

def promedio(lista):
	suma = 0
	for i in lista:
		suma += i
	prom = float(suma) / float(len(lista))
	return int(math.ceil(prom))
	
#Implementacion basada en la descripcion de Wikipedia y la respuesta de Stack Overflow
#http://en.wikipedia.org/wiki/Median#Medians_for_samples
#http://stackoverflow.com/questions/24101524/finding-median-of-list-in-python/24101655#24101655

def absolute_deviation(mediana, lista):
	new_lista = []
	for element in lista:
		ad = abs(element - mediana)
		new_lista.append(ad)
	return new_lista
	
def median_absolute_deviation(lista):
	median = mediana(lista)
	abs_dev = absolute_deviation(median, lista)
	mad = mediana(abs_dev)
	prom = promedio(lista)
	prom_n = promedio(abs_dev)
	print "median", median, "mad", mad, abs_dev[len(abs_dev) - 1], prom, prom_n
	return mad
	

def mediana(lista):
	for i in xrange(0, 10):
		print lista[i]
	lista.sort
	for i in xrange(0, 10):
		print lista[i]
	if len(lista) % 2 == 0:
		suma = lista[(len(lista) / 2) - 1] + lista[len(lista)/2]
		mediana_par =  math.ceil(suma / 2.0)
		return int(mediana_par)
	else:
		return lista[((len(lista) + 1)/2) - 1]

def existe_archivo(argv):
	if len(argv) > 1:
		filename = argv[len(argv) - 1]
		if os.path.isfile(filename):
			return True
		else:
			print "No existe archivo '{}'".format(filename)
			return False
		
#http://stackoverflow.com/a/3964691
def traer_archivos(dir, file_ext):
	archivos = []
	for file in os.listdir(dir):
		if file.endswith(file_ext):
			archivos.append(file)
	return archivos
			
