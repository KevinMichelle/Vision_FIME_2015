import math

def standard_deviation(elements):
	n = len(elements)
	average_sample = average(elements)
	suma = 0
	for element in elements:
		suma += math.pow(element - average_sample, 2)
	aux = (1.0/(n - 1.0)) * (suma)
	return math.sqrt(aux)

def average(elements):
	new_sum = 0
	for element in elements:
		new_sum += element
	average = float(new_sum) / float(len(elements))
	return average

def euclidean_distance(pointa, pointb):
	new_sum = 0
	if (type(pointa) == list or type(pointa) == tuple) and (type(pointb) == list or type(pointb) == tuple):
		if len(pointa) == len(pointb):
			for i in xrange(len(pointa)):
				aux = pointb[i] - pointa[i]
				new_sum += pow(aux, 2)
	elif (type(pointa) == int or type(pointa) == float) and (type(pointb) == int or type(pointb) == float):
		aux = pointb - pointa
		new_sum += pow(aux, 2)
	else:
		print "Error Euclidean Distance"
		quit()
		return None
	return math.sqrt(new_sum)
	
#Implementacion basada en la descripcion de Wikipedia y la respuesta de Stack Overflow
#http://en.wikipedia.org/wiki/Median#Medians_for_samples
#http://stackoverflow.com/questions/24101524/finding-median-of-list-in-python/24101655#24101655
def median(elements):
	if type(elements) is list:
		elements.sort()
		if len(elements) % 2 == 0:
			new_sum = elements[(len(elements) / 2) - 1] + elements[len(elements)/2]
			median =  math.ceil(new_sum / 2.0)
			return median
		else:
			median = elements[((len(elements) + 1)/2) - 1]
			return median
	else:
		return None 
		
def mode(elements):
	if type(elements) is list:
		elements_dictio = {}
		for element in elements:
			if element not in elements_dictio:
				elements_dictio[element] = 1
			else:
				elements_dictio[element] += 1
		mode = 0
		for element_key in elements_dictio:
			value = elements_dictio[element_key]
			if value > mode:
				mode = element_key
	return mode
		
def median_absolute_deviation(elements):
	median = median(elements)
	new_elements = []
	for element in elements:
		abs_dev = (element - median)
		new_elements.append(abs_dev)
	new_median = median(new_elements)
	return new_median