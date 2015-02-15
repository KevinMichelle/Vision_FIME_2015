from PIL import Imageimport randomimport colorsysimport auxiliary as auxdef escala_grises(imagen):	xs, ys = imagen.size	pixeles = imagen.load()	nueva_imagen = imagen.copy()	pixeles_nuevos = nueva_imagen.load()	for y in xrange(ys):		for x in xrange(xs):			pixel = pixeles[x, y]			promedio = (pixel[0] + pixel[1] + pixel[2]) / 3			pixeles_nuevos[x, y] = (promedio, promedio, promedio)	return nueva_imagen	#http://en.wikipedia.org/wiki/HSL_and_HSV#Examplesdef new_color():	min_value, max_value = 0.2, 0.9	rgb_max_value = 255	h = (random.uniform(0, 360))/360 #hue	l = random.uniform(min_value, max_value) #lightness	s = random.uniform(min_value, max_value) #saturation	r, g, b = colorsys.hls_to_rgb(h, l, s)	r = int(r * rgb_max_value)	g = int(g * rgb_max_value)	b = int(b * rgb_max_value)	return (r, g, b)def color_is_distinct(colors, newcolor):	bool_distance = False	for color in colors:		distance = aux.euclidean_distance(color, newcolor)		if distance < 50:			bool_distance = True			break	return bool_distance	def gen_color(colors):	bool_check = False	if type(colors) == list:		if len(colors) > 0:			bool_check = True	newcolor = new_color()	if bool_check:		bool_distance = color_is_distinct(colors, newcolor)		while bool_distance:			newcolor = new_color()			bool_distance = color_is_distinct(colors, newcolor)	return newcolor