# Camera calibration

We use a simple checkerboard to obtain camera intrinsic properties and distortion parameters.

## Run

### Create virtual environment
It's advised to create a conda environment first.
```shell script
conda create -n camera python=3.8
conda init
exec zsh
conda activate camera
```
### Clone repository
```shell script
git clone https://github.com/yashdeep01/CameraCalibrationCheckerboard.git
cd CameraCalibrationCheckerboard/
```
### Install requirements
```shell script
pip install -r requirements.txt
```

## File structure
Cloning the repo must give you such a directory tree
```shell script
├── CameraCalibrationCheckerboard
│   ├── README.md
│   ├── calibrate.py
│   ├── checkerboard/
│   ├── extract_frames.py
│   ├── frames/
│   └── requirements.txt
```

### Populate directories
Before running calibration on your machine, you must click some pictures of the chekcerboard given as `pattern.pdf` here. Follow the steps:
1. Print the checkerboard pattern on an A4 sheet.
2. Glue the pattern on a flat surface, like a wall, cardboard, etc.
3. Keep the surface still and click its photos from various angles. Click at least 50 images. Alternatively, you could also record a video by moving the camera around the surface at various angles and distance.
4. Save the photos (or video) on your machine.
    - If you clicked pictures, save the clicked pictures in `./frames/` directory of the cloned repo.
    - Else, if you recorded a video, run this command to extract frames from the video and automatically save in `./frames/` directory:
    ```shell script
    python extract_frames.py --video /path/to/video
   ```

### Run camera calibration
```shell script
python calibrate.py
```
Aruco markers drawn on the checkerboard photos are stored in `./checkerboard/` directory.

The results of the calibration command are present in `./results/` directory.
- `./results/mtx.csv` contains the `3x3` [camera intrinsic matrix](https://developer.apple.com/documentation/avfoundation/avcameracalibrationdata/2881135-intrinsicmatrix) (denoted by _**K**_).
- `./results/dist.csv` contains the distortion parameters _k1, k2, k3..._ which are responsible for the fish-eye effect in the images captured by the camera.
- `./results/rvecs.csv` contains the rotation vectors **R** of the [camera extrinsic matrix](https://developer.apple.com/documentation/avfoundation/avcameracalibrationdata/2881130-extrinsicmatrix).
- `./results/tvecs.csv` contains the translation vectors **t** of the [camera extrinsic matrix](https://developer.apple.com/documentation/avfoundation/avcameracalibrationdata/2881130-extrinsicmatrix).

### Optional commands
This package allows users many flexibilities while performing calibration. Running `python calibrate.py --help` gives the following output on shell:

```bash
 % python calibrate.py --help
usage: calibrate.py [-h] [-p PATH] [-r ROW] [-c COL]

Calibrate a camera using checkerboard

optional arguments:
  -h, --help            show this help message and exit
  -p PATH, --path PATH  Path of the images directory
  -r ROW, --row ROW     No. of rows of the checkerboard
  -c COL, --col COL     No. of cols of the checkerboard

```
   
## Acknowledgements
- OpenCV camera calibration [docs](https://docs.opencv.org/master/dc/dbb/tutorial_py_calibration.html).
- Checkerboard pattern provided by [boofcv](https://boofcv.org/index.php?title=Camera_Calibration_Targets).