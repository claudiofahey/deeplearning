
# Image Generator

image_generator.py will read a directory of images, apply various random transformations, and then write the images to a new directory.

It will process images in parallel on a single host (use --parallelism).

It will also retrain the directory structure for a certain number of levels.
With `--output_dir_depth 1` for example, the source image `input_dir/tulip/tuplip1.jpg` will be transformed and written to
`output_dir/tulip/tulip1-fa13fb9e-bf9e-4047-a6d5-3111b4b1b01a.jpg`. 
This ensures that the images retain their labels.

A Dockerfile has been created to ensure that the necessary dependencies (opencv) are available.
The file `run.sh` shows how to build the Docker container and execute it on the
flower data set (http://download.tensorflow.org/example_images/flower_photos.tgz).

# References

- <https://github.com/damianmoore/tensorflow-image-classifier>
