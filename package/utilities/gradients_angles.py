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

	
#changes in the key of angles, maybe I will need to check possibles errors in previous programs
def define_angles(gradients, discretize_option):
	pi = math.pi
	angles = {}
	if discretize_option == 1: #range of angles is larger
		discret_angles = [0, pi/8.0, pi/4.0, (3.0*pi)/8.0, pi/2.0, (5.0*pi)/8.0, (3*pi)/4.0, (7.0*pi)/8.0, pi]
	elif discretize_option == 2: #range of angles is lesser
		discret_angles = [0, pi/4.0, pi/2.0,(3*pi)/4.0, pi]
	elif discretize_option == 3:
		discret_angles = []
		aux = 0
		discret_angles.append(aux)
		while aux <= pi:
			aux += (pi/256.0)
			discret_angles.append(aux)
	for gradient in gradients:
		y, x = gradient[0], gradient[1]
		normal_angle, slope_angle = gradients[gradient][1], gradients[gradient][4]
		normal_angle, slope_angle = normal_angle % (pi), slope_angle % (pi)
		if discretize_option == 0:
			new_normal_angle, new_slope_angle = normal_angle, slope_angle
		else:
			new_normal_angle, new_slope_angle = discretize_angle(discret_angles, normal_angle), discretize_angle(discret_angles, slope_angle)
		gradients[gradient][1] = new_normal_angle
		gradients[gradient][4] = new_slope_angle
		if gradient not in angles:
			angles[gradient] = 1
		else:
			angles[gradient] += 1
	return angles