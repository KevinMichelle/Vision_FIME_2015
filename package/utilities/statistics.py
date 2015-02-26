import math

def average(elements):
	new_sum = 0
	for element in elements:
		new_sum += element
	average = float(new_sum) / float(len(elements))
	return average

def euclidean_distance(pointa, pointb):
	if len(pointa) == len(pointb):
		new_sum = 0
		for i in xrange(len(pointa)):
			aux = pointb[i] - pointa[i]
			new_sum += pow(aux, 2)
		return math.sqrt(new_sum)	
	return None
	
#Implementacion basada en la descripcion de Wikipedia y la respuesta de Stack Overflow
#http://en.wikipedia.org/wiki/Median#Medians_for_samples
#http://stackoverflow.com/questions/24101524/finding-median-of-list-in-python/24101655#24101655
def median(elements):
	if type(elements) is tuple:
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
		
def median_absolute_deviation(elements):
	median = median(elements)
	new_elements = []
	for element in elements:
		abs_dev = (element - median)
		new_elements.append(abs_dev)
	new_median = median(new_elements)
	return new_median