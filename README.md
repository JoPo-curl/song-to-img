# song-to-img

Just a simple script to automize generating stable diffusion images from song lyrics using automatic1111's api

In the basic configuration it will generate 12 images, a combo of cfg values 3,6,9,12 and steps 20, 28, 60 and random seeds
It will take the texts of any file in the lyrics folder and use as prompts, one a file has generated all 12 images its moved to the done folder.