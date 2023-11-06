# fractal_dimension_and_DLA
1. Python OpenCV and box-counting (Minkowski–Bouligand) method for calculating the fractal dimension of an object in the image. 
fractal_dim_final.py - contains just the functions to determine the fractal dimensions of an object in the image 
helpscripts.py - additional utility scripts I used, to automate the experimental data processing

2. Diffusion Limited Aggregation algorithm
DLA_clean.py - all of the code to perform diffusion limited aggregation algorithm simulation. Includes two versions, a one-by-one walker release (simple) and a many-at-once walkers release (batch) which was done to finetune the algorithm to experimental results (according to the fractal dimensions of the fractal-droplet formed)


I wrote this program when conducting research on viscous fingering, so this repository also includes some code to detect the radius of the circular object (the fractal I was investigating in my case), and to apply these functions to a video by splitting it into frames.
In the 'photo and video examples' folder, I attach some of the images I used my program to process. Changing some of the image preprocessing parameters might be needed for different images. 


