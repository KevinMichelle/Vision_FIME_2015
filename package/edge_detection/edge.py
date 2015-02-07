from PIL import Image
import sys
import os.path
import math
import rutinas
import routines.routines as routines
import routines.auxiliary as auxiliary

def __main__(filename):
	imagen_original = Image.open(filename)
	imagen_original = imagen_original.convert('RGB')
	imagen_grises = procesamiento.escala_grises(imagen_original)

if __name__ == '__main__':
	existe = rutinas.existe_archivo(sys.argv)
	if existe:
		__main__(sys.argv[len(sys.argv) - 1])