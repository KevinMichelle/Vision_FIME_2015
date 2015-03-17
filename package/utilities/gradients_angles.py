import math
import utilities.statistics as statistics

def discretize_angle(discret_angles, angle):
	max_distance = math.pi
	new_angle = 0.0
	for discret_angle in discret_angles:
		distance_angle = statistics.euclidean_distance(angle, discret_angle)
		if distance_angle <= max_distance:
			max_distance = distance_angle
			new_angle = discret_angle
	return new_angle

	
def define_angles(gradients, discretize_option):
	pi = math.pi
	angles = {}
	if discretize_option == 1: #range of angles is larger
		discret_angles = [0, pi/8.0, pi/4.0, (3.0*pi)/8.0, pi/2.0, (5.0*pi)/8.0, (3*pi)/4.0, (7.0*pi)/8.0, pi]
	elif discretize_option == 2: #range of angles is lesser
		discret_angles = [0, pi/4.0, pi/2.0,(3*pi)/4.0, pi]
	for gradient in gradients:
		y, x = gradient[0], gradient[1]
		aux_angle = gradients[gradient][1]
		angle = aux_angle % pi
		if discretize_option == 0:
			new_angle = angle
		else:
			new_angle = discretize_angle(discret_angles, angle)
		gradients[gradient][1] = new_angle
		if new_angle not in angles:
			angles[new_angle] = 1
		else:
			angles[new_angle] += 1
	return angles