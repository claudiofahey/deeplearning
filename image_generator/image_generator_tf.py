
# import tensorflow as tf
# import numpy as np
import os

import numpy as np
import tensorflow as tf
from tensorflow.python.framework import graph_util
from tensorflow.python.framework import tensor_shape
from tensorflow.python.platform import gfile
from tensorflow.python.util import compat


def modify_image(image):
    resized = tf.image.resize_images(image, (180, 180), align_corners=True)
    resized.set_shape([180,180,3])
    flipped_images = tf.image.flip_up_down(resized)
    return flipped_images

def read_image(filename_queue):
    reader = tf.WholeFileReader()
    key,value = reader.read(filename_queue)
    image = tf.image.decode_jpeg(value)
    return key,image

def inputs():
    # filenames = ['img1.jpg', 'img2.jpg' ]
    # file_glob = '../data/*.jpg'
    file_glob = '../data/tf_files/flowers/data/*/*.jpg'
    filenames = gfile.Glob(file_glob)
    print('filenames=%s' % str(filenames))
    filename_queue = tf.train.string_input_producer(filenames, num_epochs=1)
    filename,read_input = read_image(filename_queue)
    reshaped_image = modify_image(read_input)
    return filename,reshaped_image

def main():
    print('Starting')
    # cur_dir = os.getcwd()
    # print("resizing images")
    # print("current directory:", cur_dir)
    with tf.Graph().as_default():
        image = inputs()
        init_op = tf.group(tf.global_variables_initializer(),
                           tf.local_variables_initializer())
        sess = tf.Session()
        sess.run(init_op)
        tf.train.start_queue_runners(sess=sess)

        try:
            while True:
                filename, img = sess.run(image)
                print('filename=%s, shape=%s' % (filename, str(img.shape)))
        except tf.errors.OutOfRangeError:
            # This will be raised when you reach the end of an epoch (i.e. the
            # iterator has no more elements).
            pass

        # for i in range(10):
            # img = Image.fromarray(img, "RGB")
            # img.save(os.path.join(cur_dir,"foo"+str(i)+".jpeg"))
    print('Done.')

if __name__ == '__main__':
    main()
