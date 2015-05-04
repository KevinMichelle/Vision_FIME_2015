import utilities.files as files
import utilities.pix as pix
import utilities.statistics as statistics
import holes.hole as hole
import sys
from PIL import Image

#colorea de negro los pixeles de una imagen si la distancia euclidiana del color original del pixel 
#con respecto a al menos un color en una lista de colores llega a ser menor o igual a un umbral predefinido
def buscar_croquetas(image, list_of_colors):
	threshold = 100
	xs, ys = image.size
	pixels = image.load()
	for y in xrange(ys):
		for x in xrange(xs):
			bool_color = False
			pixel_value = pixels[x, y]
			for color_sample in list_of_colors:
				distance = statistics.euclidean_distance(pixel_value, color_sample)
				if distance <= threshold:
					bool_color = True
			if bool_color:
				pixels[x, y] = (0, 0, 0)
			else:
				pixels[x, y] = (255, 255, 255)
	return image

#http://www.rapidtables.com/web/color/brown-color.htm colores cafe
def __main__(filename, choice_save):
	blackcolor = (0, 0, 0)
	list_of_colors = [(218,165,32), (205,133,63), (210,105,30), (139,69,19), (160,82,45), (165,42,42), (128,0,0)] #lista de colores
	original_image = Image.open(filename)
	rgb_image = original_image.convert('RGB')
	image = pix.grayscale_image(rgb_image)
	food_image = buscar_croquetas(rgb_image, list_of_colors)
	frec_colors = pix.frec_colors(food_image)
	xs, ys = food_image.size
	total_pixels = xs * ys
	black_frec = frec_colors[blackcolor]
	black_porc = (black_frec * 100) / float(total_pixels)
	print "Porcentaje: ", black_porc, "%"
	if black_porc >= 75.0:
		print "Exceso de comida"
	elif black_porc >= 55.0:
		print "Suficiente comida"
	elif black_porc > 20.0:
		print "Insuficiente comida, no seas mal amo"
	else:
		print "Eres una escoria"
	if choice_save[0]:
		bool_save =  files.validate_save("carepet\\", choice_save[1], '.png')
		if bool_save[0]:
			print "Directory of the new image: {}".format(bool_save[1])
			food_image.save(bool_save[1])			
	return None
	
#run in the 'package' directory
if __name__ == '__main__':
	pre_options = files.validate_arguments(sys.argv)
	__main__(pre_options[0], pre_options[2])