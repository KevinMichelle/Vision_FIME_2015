import sys


# Explanation about the 'dict_to_list' function
#
# We know that the basic element in a dictionary structure is a tuple: the key and their value corresponding to that key. 
#
# The key must be hashable, so it may be a number, a tuple, things like that. If am not in a mistake, the value of can be anything.
#
# So, suppose I have the following dictionary
#
#	Hello = {}
#	Hello[1] = 10
#	Hello[2] = 7
#	Hello[3] = 5
#
# If print the dictionary it would be like this
#
# Hello = {1:10, 2:7, 5:7}
#
# I like use dictionary to check the frecuency of a certain colecction of items. It seems so natural do this task with dictionary.
#  But also I find difficult to do certain statistics things with a dictionary.
#
# So maybe you can try the following process:
#	"build" your structure as a dictionary because it is easier
#	convert the dictionary structure to a list.
#
# I find three situations about this process converting.
#	1 - You dont care about the keys in the dictionary, only the values
#		Example: 10, 7, 5
#	2 - You care only the keys
#		Example: 1, 2, 3
#	3 - You care both the key and their value and want see how many times a element repeats
#		Example: 1 1 1 1 1 1 1 1 1 1 2 2 2 2 2 2 2 3 3 3 3 3
#
# The 'bool_key' variable is a boolean that defines the flow of how you want convert the dictionary.
# If it is true, definitely you want that the keys be in the list. If it is false, then you only will see their values, like in the case 1.
# And the 'bool_dictio' variable is another boolean that only affecs the flow of the progam in if the 'bool_key' variable is true.
# If it is true then you will see the list like in the case 3. If is is false, then it will be like in the case 2.

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