Hi, this software implements many function of image processing functions, if you want to try a special function please read this document.

-- All commands must be run in the 'package' directory --

I - Filters

II - Masks

III - Edge detection

	-A basic edge detection needs the following command:

		python -m edge_detection.mascaras -o sobeldg INPUTFILE
		
		
	NOTE: If you want to try another mask, or create another mask, please replace 'sobeldg' with the name of the file of this mask in this directory: 
			your_previous_directory\Vision_FIME_2015\package\edge_detection\masks\special
			
IV - Form detection

	python -m forms.floodfill INPUTFILE
	
NOTE
	If you want to save the new image please add the '-s' option and later the name of the new file in the command that you run.

		Example:
		
		python -m forms.floodfill -s NEWNAME INPUTFILE
		
	The new images is going to be saved in the 'dest' directory inside the package: