from matplotlib import pyplot
from mtcnn.mtcnn import MTCNN

import os
# error fixes
# FIXED :sudo ln -s /usr/local/cuda-11.0/targets/x86_64-linux/lib/libcusolver.so.11 /home/piotr/Documents/medus/venv/lib/python3.8/site-packages/tensorflow/python/libcusolver.so.11
# @reboot root for a in /sys/bus/pci/devices/*; do echo 0 | tee -a $a/numa_node; done > /dev/null  APPEND TO  /etc/crontab

os.environ['CUDA_VISIBLE_DEVICES'] = "0"


# draw each face separately
def draw_faces(filename, result_list):
    # load the image
    data = pyplot.imread(filename)
    # plot each face as a subplot
    for i in range(len(result_list)):
        # get coordinates
        x1, y1, width, height = result_list[i]['box']
        x2, y2 = x1 + width, y1 + height
        # define subplot
        pyplot.subplot(1, len(result_list), i + 1)
        pyplot.axis('off')
        # plot face
        pyplot.imshow(data[y1:y2, x1:x2])
    # show the plot
    pyplot.show()


filename = 'forum.jpg'
pixels = pyplot.imread(filename)
detector = MTCNN()
faces = detector.detect_faces(pixels)
draw_faces(filename, faces)
