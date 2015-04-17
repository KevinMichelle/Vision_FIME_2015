#INTRO

Hi, this software implements many function of image processing functions, if you want to try a special function please read this document.

All commands must be run in the 'package' directory inside this repository.

#WHAT'S NEW ON THE REPOSITORY#

Circle detection (Improved!)  
![Circle](https://github.com/KevinMichelle/Vision_FIME_2015/blob/master/package/circles/output/sample1.png)
Ellipse detection (Improved!)  
![Ellipse](https://github.com/KevinMichelle/Vision_FIME_2015/blob/master/package/ellipses/output/sample1.png)
Hole detection (New!)  
![Hole](https://github.com/KevinMichelle/Vision_FIME_2015/blob/master/package/holes/output/sample1.png)
	
#HOW TO SAVE THE NEW IMAGE

If you want to save the new image please add the '-s' option and later the name of the new file in the command that you run.

	python -m examples.example -s NEWNAME INPUTFILE
	
The new image will be saved in the 'output' directory inside the directory where is located the main function of the program that was executed.

For example, in the previous command the new image will be saved in this directory:

	your_previous_directory\Vision_FIME_2015\package\edges\output\

**I - Edge detection**

	python -m edges.edge INPUTFILE
	
By default the program use the Sobel masks. If you want to try another mask, please add the '-o' option and later the name of the mask according to th filenames of this directory: 
	
	your_previous_directory\Vision_FIME_2015\package\utilities\masks\special\
	
Also, you can add new masks (only DG masks, sorry!) if you want.

**II - Shape detection**

	python -m shapes.shape INPUTFILE

By default the program only shows the shapes in the new image, but if you add the '-o' option to the command, it will print in the command line interface information about the shapes that were found in the image. 
	
Also, the program will draw this information in the new image for better visualization.

**III - Line detection**

	python -m lines.line INPUTFILE

**IV - Circle detection**

	python -m circles.circle INPUTFILE
	
**V - Ellipse detection**

	python -m ellipses.ellipse INPUTFILE
	
**VI - Hole detection**

	python -m holes.hole INPUTFILE