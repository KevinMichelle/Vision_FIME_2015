import os

def validate_arguments(arguments):
	filename = arguments[len(arguments) - 1]
	exists = file_exists(filename)
	if exists:
		choice_option = (None, None)
		choice_save = (None, None)
		if len(arguments) > 2:
			for index_argument in xrange(len(arguments) - 1):
				argument = arguments[index_argument]
				if argument == "-o" or argument == "o" or argument == "-O" or argument == "O":
					if index_argument < len(arguments):
						choice_option = (True, arguments[index_argument + 1])
				if argument == "-s" or argument == "S" or argument == "-S" or argument == "S":
					if index_argument < len(arguments):
						choice_save = (True, arguments[index_argument + 1])
		else:
			choice_option, choice_save = (False, None), (False, None)
		return (arguments[len(arguments) - 1], choice_option, choice_save)
	else:
		print "There not exists a file '{}'".format()
		quit()

def validate_filename(filename):
	bool_filename = True
	for letter in filename:
		value = ord(letter)
		if not (value >= 48 and value <= 57):
			if not(value >= 65 and value <= 90):
				if not (value >= 97 and value <= 122):
					bool_filename = False
					return bool_filename
	return bool_filename

def file_exists(filename):
	if os.path.isfile(filename):
		return True
	else:
		return False
		
def validate_save(directory, filename, extension):
	bool_save = (False, None)
	full_filename = directory + filename + extension
	bool_name = validate_filename(filename)
	if bool_name:
		exists_name = file_exists(full_filename)
		if not exists_name:
			bool_save = (True, full_filename)
		else:
			dummy = 1
			new_name = ""
			while exists_name:
				new_name = full_filename[0:len(full_filename)-4] + str(dummy) + ext
				dummy += 1
				exists_name = file_exists(new_name)
			bool_save = (True, new_name)
	else:
		print 'Illegal characters in the name: {}'.format(filename)
	return bool_save
		
#http://stackoverflow.com/a/3964691
def find_files(directory, extension):
	new_files = []
	for file in os.listdir(directory):
		if file.endswith(extension):
			new_files.append(file)
	return new_files
