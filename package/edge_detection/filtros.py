from PIL import Image
import sys
import routines.routines as rout
import routines.auxiliary as aux

def aplicar_filtro(imagen, tipo_filtro):
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
				nuevo_valor = aux.mediana(vecinos_valores)
			if tipo_filtro == 1: #promedio
				nuevo_valor = aux.promedio(vecinos_valores)
			pixeles_nuevos[x, y] = (nuevo_valor, nuevo_valor, nuevo_valor)
	return nueva_imagen
				

def __main__(filename, choice_filter, choice_save):
	filter_to_use = 0 #default
	if choice_filter[0]:
		bool_filter = False
		filter_name = choice_filter[1]
		if filter_name == "median":
			filter_to_use = 0
			bool_filter = True
		elif filter_name == "mean":
			filter_to_use = 1	
			bool_filter = True
		if bool_filter:
			print "Filter to use: {}".format(filter_name)
		else:
			print "Default filter: median"
	imagen_original = Image.open(filename)
	imagen_original = imagen_original.convert('RGB')
	imagen_grises = rout.escala_grises(imagen_original)
	new_image = aplicar_filtro(imagen_grises, filter_to_use)
	if choice_save[0]:
		bool_save =  aux.checar_guardar("dest\\", choice_save[1], '.png')
		if bool_save[0]:
			print "Directory of the new image: {}".format(bool_save[1])
			new_image.save(bool_save[1])
	new_image.show()
	return None

if __name__ == '__main__':
	pre_options = aux.pre_argv(sys.argv)
	__main__(pre_options[0], pre_options[1], pre_options[2])
