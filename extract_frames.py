import cv2

import os
import argparse
import time
import shutil


parser = argparse.ArgumentParser(allow_abbrev=False,
                                 description='Extract and save frames from a video')
parser.add_argument('-v', '--video',
                    type=str,
                    help='Path of the video')
parser.add_argument('-d', '--dir',
                    type=str,
                    default='./frames/',
                    help='Path of image directory')
args = parser.parse_args()


def extract(path_video, path_images):
    if os.path.exists(path_images):
        shutil.rmtree(path_images)
    os.makedirs(path_images)

    images = []
    vidcap = cv2.VideoCapture(path_video)
    success, image = vidcap.read()
    count = 0

    images.append(image)

    while success:
        cv2.imwrite(os.path.join(path_images, "frame%d.jpg" % count), image)  # save frame as JPG file
        success, image = vidcap.read()
        if type(image) is not type(images[0]):
            break
        images.append(image)
        print(f'Read a new frame: {success}, frame{count}.jpg')
        count += 1

    print(f"\nCount of successful frames: {count + 1}")


if __name__ == "__main__":
    path_video = args.video
    path_images = args.dir
    t1 = time.time()
    extract(path_video, path_images)
    print(f"\n{time.time() - t1} seconds\n")