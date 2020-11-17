import cv2
import numpy as np

import os
import argparse
import time
import glob

parser = argparse.ArgumentParser(allow_abbrev=False,
                                 description='Calibrate a camera using checkerboard')
parser.add_argument('-p', '--path',
                    type=str,
                    default='./frames/',
                    help='Path of the images directory')
parser.add_argument('-r', '--row',
                    type=int,
                    default=5,
                    help='No. of rows of the checkerboard')
parser.add_argument('-c', '--col',
                    type=int,
                    default=8,
                    help='No. of cols of the checkerboard')
args = parser.parse_args()


def calibrate(path, dims):
    # Defining the dimensions of checkerboard
    CHECKERBOARD = dims
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

    # Creating vector to store vectors of 3D points for each checkerboard image
    objpoints = []
    # Creating vector to store vectors of 2D points for each checkerboard image
    imgpoints = []

    # Defining the world coordinates for 3D points
    objp = np.zeros((1, CHECKERBOARD[0] * CHECKERBOARD[1], 3), np.float32)

    objp[0, :, :2] = np.mgrid[0:CHECKERBOARD[0], 0:CHECKERBOARD[1]].T.reshape(-1, 2)
    objp = objp * 0.03  # each square is 0.03 m per side (or 3 cm)

    path_checkerboard = "./checkerboard/"
    if os.path.exists(path_checkerboard):
        shutil.rmtree(path_checkerboard)
    os.makedirs(path_checkerboard)

    count = 0
    gray = None
    for fname in glob.glob(os.path.join(path, "*")):
        image = cv2.imread(fname)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # Find the chess board corners
        # If desired number of corners are found in the image then ret = true
        ret, corners = cv2.findChessboardCorners(gray, CHECKERBOARD,
                                                 cv2.CALIB_CB_ADAPTIVE_THRESH
                                                 + cv2.CALIB_CB_FAST_CHECK
                                                 + cv2.CALIB_CB_NORMALIZE_IMAGE)

        """
        If desired number of corner are detected,
        we refine the pixel coordinates and display 
        them on the images of checkerboard.
        """
        if ret is True:
            objpoints.append(objp)
            # refining pixel coordinates for given 2d points.
            corners2 = cv2.cornerSubPix(gray, corners, (11, 11), (-1, -1), criteria)

            imgpoints.append(corners2)

            # Draw and display the corners
            image = cv2.drawChessboardCorners(image, CHECKERBOARD, corners2, ret)
            cv2.imwrite(os.path.join(path_checkerboard, "aruco_%d.jpg" % count), image)
            print(f"Saved ./checkerboard/aruco_{count}.jpg")

        count += 1

    cv2.destroyAllWindows()
    """
    Performing camera calibration by 
    passing the value of known 3D points (objpoints)
    and corresponding pixel coordinates of the 
    detected corners (imgpoints)
    """
    ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, gray.shape[::-1], None, None)

    if os.path.exists('./results/'):
        shutil.rmtree('./results/')
    os.makedirs('./results/')

    print("Camera matrix : \n")
    print(mtx)
    np.savetxt('./results/mtx.csv', mtx, delimiter=',')
    print("dist : \n")
    print(dist)
    np.savetxt('./results/dist.csv', dist, delimiter=',')
    print("rvecs : \n")
    print(rvecs)
    np.savetxt('./results/rvecs.csv', rvecs, delimiter=',')
    print("tvecs : \n")
    print(tvecs)
    np.savetxt('./results/tvecs.csv', tvecs, delimiter=',')


if __name__ == "__main__":
    path = args.path
    dims = tuple((args.row, args.col))
    t1 = time.time()
    calibrate(path, dims)
    print(f"\nTime taken: {time.time() - t1} seconds\n")