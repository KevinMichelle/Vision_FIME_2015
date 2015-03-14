import sys
from PIL import Image
import edges.edge as edge
import shapes.shape as shape
import utilities.files as files
import utilities.pix as pix
import utilities.gradients_angles as gradients_angles

def define_circles(image):
	mask_to_use = "prewittdg"
	shape_image_info = shape.floodfill(image)
	shape_image, shape_info = shape_image_info[0], shape_image_info[1]
	gradients = edge.find_edges(shape_image, mask_to_use, False)
	angles = gradients_angles.define_angles(gradients, 0)
	shape_image = edge.draw_edges(shape_image, gradients, False)
	shape_image = shape.draw_shapes_info(shape_image, shape_info)
	print len(gradients)
	shape_image.show()
	for shape_info_key in shape_info:
		info = shape_info[shape_info_key]
		y_shape, x_shape = info[0][0], info[0][1]
		center = info[1]
		print y_shape, x_shape, center
		lower_y, upper_y = y_shape[0], y_shape[1]
		lower_x, upper_x = x_shape[0], x_shape[1]
		edge_shape = {}
		for y in xrange(lower_y, upper_y + 1):
			for x in xrange(lower_x, upper_x + 1):
				check = (y, x)
				if check in gradients:
					edge_shape[check] = gradients[check]
		print "gradientes, figura"
		print len(edge_shape)
		angles = gradients_angles.define_angles(edge_shape, 1) #less angles
		print angles
	quit()
	return image

def __main__(filename, choice_info, choice_save):
	bool_info = False
	choice_info = False #dummy
	original_image = Image.open(filename)
	rgb_image = original_image.convert('RGB')
	image = pix.grayscale_image(rgb_image)
	circle_image = define_circles(image)
	circle_image.show()
	if choice_save[0]:
		bool_save =  files.validate_save("lines\output\\", choice_save[1], '.png')
		if bool_save[0]:
			print "Directory of the new image: {}".format(bool_save[1])
			circle_image.save(bool_save[1])			
	return None
	
#run in the 'package' directory
if __name__ == '__main__':
	pre_options = files.validate_arguments(sys.argv)
	__main__(pre_options[0], pre_options[1], pre_options[2])