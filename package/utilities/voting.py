import utilities.structures as structures
import utilities.statistics as statistics
import utilities.neighbors as neighbors
import random

def voting_process(voting_pixels_dict, pixels, ys, xs):
	change_number_possible = True
	axis_limits = (ys, xs)
	while change_number_possible:
		number_before = len(voting_pixels_dict)
		frec_voting_pixels = structures.dict_to_list(voting_pixels_dict, False, False)
		average_voting_pixels = statistics.average(frec_voting_pixels)
		possible_centers_list = possible_centers(voting_pixels_dict, average_voting_pixels)
		for center in possible_centers_list:
			center_value = voting_pixels_dict[center]
			neighbor_pixels = neighbors.find_neighbors(pixels, center, None, axis_limits)
			for neighbor in neighbor_pixels:
				pixel_neighbor = neighbor[0]
				if pixel_neighbor in voting_pixels_dict:
					if pixel_neighbor != center:
						neighbor_value = voting_pixels_dict[pixel_neighbor]
						if neighbor_value < center_value:
							voting_pixels_dict[center] += voting_pixels_dict[pixel_neighbor]
		remove_not_possible_centers(voting_pixels_dict, possible_centers_list)
		number_after = len(voting_pixels_dict)
		if number_after == number_before:
			change_number_possible = False
	print voting_pixels_dict
	champion = random.choice(voting_pixels_dict.keys())
	return champion
	
def remove_not_possible_centers(voting_pixels_dict, possible_centers_list):
	not_possible_centers = list()
	for pixel in voting_pixels_dict:
		if pixel not in possible_centers_list:
			not_possible_centers.append(pixel)
	for not_center in not_possible_centers:
		del voting_pixels_dict[not_center]
	return None
	
def possible_centers(voting_pixels_dict, average_voting_pixels):
	possible_centers_list = []
	for voting_pixel in voting_pixels_dict:
		if voting_pixels_dict[voting_pixel] >= average_voting_pixels:
			possible_centers_list.append(voting_pixel)
	return possible_centers_list
	
def update_pixels_voting(bounding_box, pixels, line_pixels, voting_pixels_dict):
	white, black = (255, 255, 255), (0, 0, 0)
	y_shape, x_shape = bounding_box
	lower_y, upper_y = y_shape[0], y_shape[1]
	lower_x, upper_x = x_shape[0], x_shape[1]
	for y in xrange(lower_y, upper_y + 1): #add all the pixels inside the figure
		for x in xrange(lower_x, upper_x + 1):
			check = (y, x)
			if check in line_pixels:
				if pixels[x, y] != white and pixels[x, y] != black:
					if check not in voting_pixels_dict:
						voting_pixels_dict[check] = 1
					else:
						voting_pixels_dict[check] += 1
	return None
