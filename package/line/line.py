from PIL import Image, ImageDraw
import sys
import math
import edge.edge as edge
import utilities.pix as pix
import utilities.files as files
import utilities.statistics as statistics

def define_lines(image):
	mask_to_use = "prewittdg"
	gradients = edge.find_edges(image, mask_to_use, False)
	print len(gradients)
	list_of_angles = {}
	angles = {}
	for gradient in gradients:
		aux_angle = gradients[gradient][1]
		angle = aux_angle % math.pi
		if angle not in angles:
			angles[angle] = 1
		else:
			angles[angle] += 1
	print angles
	print "mod"
	print angles_mod
	return None

def __main__(filename, choice_info, choice_save):
	bool_info = False
	choice_info = False #dummy
	original_image = Image.open(filename)
	rgb_image = original_image.convert('RGB')
	image = pix.grayscale_image(rgb_image)
	shape_image = define_lines(image)
	shape_image.show()
	if choice_save[0]:
		bool_save =  files.validate_save("shape\output\\", choice_save[1], '.png')
		if bool_save[0]:
			print "Directory of the new image: {}".format(bool_save[1])
			shape_image.save(bool_save[1])			
	return None
	
#run in the 'package' directory
if __name__ == '__main__':
	pre_options = files.validate_arguments(sys.argv)
	__main__(pre_options[0], pre_options[1], pre_options[2])