import sys

def dict_to_list(structure, bool_key, bool_dictio):
	if type(structure) is dict:
		new_list = []
		if bool_key:
			for element in structure:
				if bool_dictio:
					new_list.append(element)
				else:
					count = structure[element]
					for dummy in xrange(count):
						new_list.append(element)
			return new_list
		else:
			for element in structure:
				new_list.append(structure[element])
		return new_list
	else:
		return None

def tuple_to_list(structure):
	if type(structure) is tuple:
		new_list = []
		for element in structure:
			new_list.append(element)
		return new_list
	else:
		return None 