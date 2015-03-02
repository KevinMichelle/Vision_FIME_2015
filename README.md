Hi, this software implements many function of image processing functions, if you want to try a special function please read this document.

	-- All commands must be run in the 'package' directory --
	
	--If it is desired save the new image, please read at the end of this document--

I - Edge detection

	A basic edge detection needs the following command:

		python -m edges.edge INPUTFILE
		
	By default the program use the Sobel masks. 
	
	If you want to try another mask, please add the '-o' option and later the name of the mask according to the filenames of this directory: 
		your_previous_directory\Vision_FIME_2015\package\utilities\masks\special\
	
	Also, you can add new masks (only DG masks) in this directory following the examples.
			
II - Shape detection
	
	A basic shape detection needs the following command:
	
		python -m shapes.shape INPUTFILE

	By default the program only shows the shapes in the new image, but if you add the '-o' option to the command, it will print in the command line interface
	information about the shapes that were found in the image. Also, the program will draw this information in the new image for better visualization.

III - Line detection

	A basic shape detection needs the following command:
		
		python -m lines.line INPUTFILE
	
HOW TO SAVE THE NEW IMAGE

	If you want to save the new image please add the '-s' option and later the name of the new file in the command that you run.

		python -m edges.edge -s NEWNAME INPUTFILE
		
	The new image will be saved in the 'output' directory inside the directory where is located the main function of the program that was executed.
	For example, in the previous command the new image will be saved in this directory:
		your_previous_directory\Vision_FIME_2015\package\edges\output\