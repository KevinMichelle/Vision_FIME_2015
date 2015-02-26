import randomimport colorsysfrom statistics import euclidean_distancedef color_generator(colors):	bool_check = False	if type(colors) == list:		if len(colors) > 0:			bool_check = True	newcolor = new_color()	if bool_check:		bool_distance = color_is_distinct(colors, newcolor)		while bool_distance:			newcolor = new_color()			bool_distance = color_is_distinct(colors, newcolor)	return newcolor	#http://en.wikipedia.org/wiki/HSL_and_HSVdef new_color():	min_value, max_value = 0.3, 0.9	rgb_max_value = 255	h = (random.uniform(0, 360))/360 #hue	l = random.uniform(min_value, max_value) #lightness	s = random.uniform(min_value, max_value) #saturation	r, g, b = colorsys.hls_to_rgb(h, l, s)	r = int(r * rgb_max_value)	g = int(g * rgb_max_value)	b = int(b * rgb_max_value)	return (r, g, b)def color_is_distinct(colors, newcolor):	bool_distance = False	for color in colors:		distance = euclidean_distance(color, newcolor)		if distance < 50:			bool_distance = True			break	return bool_distance