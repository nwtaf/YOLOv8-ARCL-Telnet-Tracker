import numpy as np
import cv2
from pathlib import Path

CHESSBOARD_SIZE = (7, 7) # Start from zero

def calibrate(chessboard_path, show_chessboard=False):
    # Convert the path to a Path object
    chessboard_path = Path(chessboard_path)

    if not chessboard_path.exists():
        raise FileNotFoundError(f'Path {chessboard_path} does not exist')

    # Logical coordinates of chessboard corners
    obj_p = np.zeros((1, CHESSBOARD_SIZE[0] * CHESSBOARD_SIZE[1], 3), np.float32)
    obj_p[0, :, :2] = np.mgrid[0:CHESSBOARD_SIZE[0], 0:CHESSBOARD_SIZE[1]].T.reshape(-1, 2)

    obj_points = []     # 3d point in real world space
    img_points = []     # 2d points in image plane.

    # Iterate through all images in the folder
    image_list = list(chessboard_path.glob('*'))
    print(f'Found {len(image_list)} images in {chessboard_path}')
    for image in image_list:
        img = cv2.imread(str(image))
        # cv2.imshow(f'{image}', img)
        # cv2.waitKey(0)
    gray = None
    for image in image_list:
        img = cv2.imread(str(image)) # THIS LINE IS not breaking the code
        if img is not None:
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            ret, corners = cv2.findChessboardCorners(gray, CHESSBOARD_SIZE,
                                                     cv2.CALIB_CB_ADAPTIVE_THRESH + cv2.CALIB_CB_FAST_CHECK + cv2.CALIB_CB_NORMALIZE_IMAGE)
            print(f'Find corners in {image.name}: {ret}')  # This line will indicate success or failure for corner detection
            if ret:
                # Refining corners position with sub-pixels based algorithm
                obj_points.append(obj_p)
                cv2.cornerSubPix(gray, corners, (3, 3), (-1, -1),
                                 (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.01))
                img_points.append(corners)
                print(f'Image {image.name} is valid for calibration')
                if show_chessboard:
                    cv2.drawChessboardCorners(img, CHESSBOARD_SIZE, corners, ret)
                    cv2.imwrite(str(chessboard_corners_path / image.name), img)
            else:
                print(f'Image {image.name} is not valid for calibration')

    k = np.zeros((3, 3))
    d = np.zeros((4, 1))
    if gray is not None:
        dims = gray.shape[::-1]
        num_valid_img = len(obj_points)
        if num_valid_img > 0:
            rvecs = [np.zeros((1, 1, 3), dtype=np.float64) for _ in range(num_valid_img)]
            tvecs = [np.zeros((1, 1, 3), dtype=np.float64) for _ in range(num_valid_img)]
            rms, _, _, _, _ = cv2.fisheye.calibrate(obj_points, img_points, gray.shape[::-1], k, d, rvecs, tvecs,
                                                    cv2.fisheye.CALIB_CHECK_COND +
                                                    # When CALIB_CHECK_COND is set, the algorithm checks if the detected corners of each images are valid.
                                                    # If not, an exception is thrown which indicates the zero-based index of the invalid image.
                                                    # Such image should be replaced or removed from the calibration dataset to ensure a good calibration.
                                                    cv2.fisheye.CALIB_RECOMPUTE_EXTRINSIC +
                                                    cv2.fisheye.CALIB_FIX_SKEW,
                                                    (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 1e-6))
        print("Found " + str(num_valid_img) + " valid images for calibration")
        return k, d, dims
    else:
        print("No valid images found for calibration")
        return None, None, None


if __name__ == '__main__':
    # Get the absolute path of the script
    script_path = Path(__file__).resolve()
    chessboard_path = script_path.parent / 'Chessboards'
    params_path = script_path.parent / 'parameters'
    params_dims_path = script_path.parent / 'parameters' / 'Dims'
    params_k_path = script_path.parent / 'parameters' / 'K'
    params_d_path = script_path.parent / 'parameters' / 'D'
    chessboard_corners_path = script_path.parent / 'Chessboards_Corners'
    
    Path(params_path).mkdir(parents=True, exist_ok=True)
    Path(chessboard_corners_path).mkdir(parents=True, exist_ok=True)
    
    K, D, Dims = calibrate(str(chessboard_path), show_chessboard=True)
    if K is not None and D is not None and Dims is not None:
        np.save(params_dims_path, np.array(Dims))
        np.save(params_k_path, np.array(K))
        np.save(params_d_path, np.array(D))
