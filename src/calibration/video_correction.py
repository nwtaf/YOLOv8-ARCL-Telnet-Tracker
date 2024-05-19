import numpy as np
import cv2
from pathlib import Path

def correct(img_in, k, d, dims):
    dim1 = img_in.shape[:2][::-1]
    assert dim1[0] / dim1[1] == dims[0] / dims[1], "Image to correct needs to have same aspect ratio as the ones used in calibration"
    map1, map2 = cv2.fisheye.initUndistortRectifyMap(k, d, np.eye(3), k, dims, cv2.CV_16SC2)
    img_out = cv2.remap(img_in, map1, map2, interpolation=cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT)
    return img_out


if __name__ == '__main__':
    # Get the absolute path of the script
    script_path = Path(__file__).resolve()
    chessboard_path = script_path.parent / 'Chessboards'
    params_path = script_path.parent / 'parameters'
    input_im_path = script_path.parent / 'distort.jpg'
    output_im_path = script_path.parent / 'undistorted.jpg'

    Dims = tuple(np.load(params_path / 'Dims.npy'))
    K = np.load(params_path / 'K.npy')
    D = np.load(params_path / 'D.npy')

    cap = cv2.VideoCapture(1)
    cap.set(3, 1280)
    cap.set(4, 720)
    correct_flag = True
    while cap.isOpened():
        _, frame = cap.read()
        if correct_flag:
            frame = correct(frame, k=K, d=D, dims=Dims)
        cv2.imshow('', frame)
        num_key = cv2.waitKey(1)
        if num_key == 13:
            correct_flag = not correct_flag
        if num_key == 27:
            break
