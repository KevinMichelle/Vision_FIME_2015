from PIL import Image
import sys
import routines.routines as routines
import routines.auxiliary as auxiliary

def aplicar_filtro(imagen, tipo_vecino, tipo_filtro):
	xs, ys = imagen.size
	pixeles = imagen.load()
	nueva_imagen = imagen.copy()
	pixeles_nuevos = nueva_imagen.load()
	for y in xrange(ys):
		for x in xrange(xs):
			vecinos_valores = []
			for dy in xrange(y - 1, y + 2):
				if dy >= 0 and dy < ys:
					for dx in xrange(x - 1, x + 2):
						if dx >= 0 and dx < xs:
							vecinos_valores.append(pixeles[dx, dy][0])
			if tipo_filtro == 0: #mediana
				nuevo_valor = auxiliary.mediana(vecinos_valores)
			if tipo_filtro == 1: #promedio
				nuevo_valor = auxiliary.promedio(vecinos_valores)
			pixeles_nuevos[x, y] = (nuevo_valor, nuevo_valor, nuevo_valor)
	return nueva_imagen
				

def __main__(filename):
	imagen_original = Image.open(filename)
	imagen_original = imagen_original.convert('RGB')
	imagen_grises = routines.escala_grises(imagen_original)
	imagen_mediana = aplicar_filtro(imagen_grises, 0, 0)
	imagen_promedio = aplicar_filtro(imagen_grises, 0, 1)
	imagen_grises.show()
	imagen_mediana.show()
	imagen_promedio.show()

if __name__ == '__main__':
	existe = auxiliary.existe_archivo(sys.argv[len(sys.argv) - 1])
	if existe:
		__main__(sys.argv[len(sys.argv) - 1])
