import numpy as np
import cv2
from pathlib import Path

def correct(img_in, k, d, dims):
    dim1 = img_in.shape[:2][::-1]
    assert dim1[0] / dim1[1] == dims[0] / dims[1], "Image to undistort needs to have same aspect ratio as the ones used in calibration"
    map1, map2 = cv2.fisheye.initUndistortRectifyMap(k, d, np.eye(3), k, dims, cv2.CV_16SC2)
    img_out = cv2.remap(img_in, map1, map2, interpolation=cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT)
    return img_out


if __name__ == '__main__':
    # Get the absolute path of the script
    script_path = Path(__file__).resolve()
    filename = 'snapshot_9.png'
    filename_no_stem = Path(filename).stem
    chessboard_path = script_path.parent / 'Chessboards'
    params_path = script_path.parent / 'parameters'
    input_im_path = script_path.parent / 'Chessboards_Corners' / f'{filename}'
    output_im_path = script_path.parent / 'undistorted'
    Path(output_im_path).mkdir(parents=True, exist_ok=True)

    Dims = tuple(np.load(params_path / 'Dims.npy'))
    K = np.load(params_path / 'K.npy')
    D = np.load(params_path / 'D.npy')

    img = cv2.imread(str(input_im_path))
    img = correct(img, k=K, d=D, dims=Dims)
    cv2.imwrite(str(output_im_path / f'{filename_no_stem}_undistorted.png'), img)
