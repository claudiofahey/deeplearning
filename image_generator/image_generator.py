#!/usr/bin/env python
#
# Generate new images by modifying input images.
#
# Written by: claudio.fahey@dell.com
#

import cv2
import numpy as np
from multiprocessing import Pool
import glob
import argparse
import os
import uuid
import pathlib


def process_image_wrapper(args):
    input_filename, options = args
    return process_image(input_filename, options)


def process_image(input_filename, options):
    # Calculate output file name.
    allparts  = pathlib.Path(input_filename).parts
    reldir = ''
    if options.output_dir_depth > 0:
        reldir = os.path.join(*allparts[(-1 - options.output_dir_depth):-1])
    input_basename = allparts[-1]
    input_root, ext = os.path.splitext(input_basename)
    output_basename = '%s-%s%s' % (input_root, uuid.uuid4(), ext)
    output_dir = os.path.join(options.output_dir, reldir)
    output_filename = os.path.join(output_dir, output_basename)

    print('%s => %s' % (input_filename, output_filename))

    # Create output directory.
    pathlib.Path(output_dir).mkdir(parents=True, exist_ok=True)

    # Read input file.
    img = cv2.imread(input_filename)
    if img is None:
        raise Exception('Unable to read file %s' % input_filename)

    #
    #  Modify image.
    #

    # Adjust brightness.
    random_brightness_range_pct = 50.0
    brightness_min = 1.0 - (random_brightness_range_pct / 100.0)
    brightness_max = 1.0 + (random_brightness_range_pct / 100.0)
    brightness_factor = np.random.uniform(low=brightness_min, high=brightness_max)
    img = img * brightness_factor

    # Rotate image.
    rot_deg = np.random.normal(scale=90.0)
    rows, cols = img.shape[0:2]
    rot_matrix = cv2.getRotationMatrix2D((cols / 2, rows / 2), rot_deg, 1)
    img = cv2.warpAffine(img, rot_matrix, (cols, rows))

    # Scale image.
    max_size = (1920, 1080)
    fx = max_size[0] / img.shape[0]
    fy = max_size[1] / img.shape[1]
    scale_factor = min(fx, fy)
    img = cv2.resize(img, None, fx=scale_factor, fy=scale_factor, interpolation=cv2.INTER_CUBIC)

    # Write output image.
    cv2.imwrite(output_filename, img)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--output_dir',
        type=str,
        # default='/tmp/output_dir',
        required=True,
        help='Path to folders of labeled images.'
    )
    parser.add_argument(
        '--output_dir_depth',
        type=int,
        default=1,
        help='Depth of directories to create within the output directory (0=flat).'
    )
    parser.add_argument(
        '--parallelism',
        type=int,
        default=1,
        help='Number of parallel threads.'
    )

    options, unparsed = parser.parse_known_args()

    filenames = unparsed
    filenames = [p for s in filenames for p in glob.glob(s)]

    # Process images in parallel.
    with Pool(options.parallelism) as p:
        p.map(process_image_wrapper, [(f, options) for f in filenames])


if __name__ == '__main__':
    main()
