import cv2
import numpy as np

# stereo images setup
left_img = cv2.imread('left_image.png', cv2.IMREAD_GRAYSCALE)
right_img = cv2.imread('right_image.png', cv2.IMREAD_GRAYSCALE)

# setup of StereoSGBM
window_size = 5
min_disp = 16
num_disp = 112 - min_disp
stereo = cv2.StereoSGBM_create(
    minDisparity=min_disp,
    numDisparities=num_disp,
    blockSize=window_size,
    P1=8 * 3 * window_size ** 2,
    P2=32 * 3 * window_size ** 2,
    disp12MaxDiff=1,
    uniquenessRatio=10,
    speckleWindowSize=100,
    speckleRange=32
)

# counting disparity
disparity_map = stereo.compute(left_img, right_img).astype(np.float32) / 16.0

#filtration for depth
disparity_map = cv2.medianBlur(disparity_map, 5)

# converting
h, w = left_img.shape[:2]
focal_length = 0.8 * w  # фокусное расстояние
Q = np.float32([[1, 0, 0, -w / 2.0],
                [0, -1, 0, h / 2.0],
                [0, 0, 0, -focal_length],
                [0, 0, 1, 0]])

points_3D = cv2.reprojectImageTo3D(disparity_map, Q)
mask_map = disparity_map > disparity_map.min()
output_points = points_3D[mask_map]
output_colors = cv2.cvtColor(left_img, cv2.COLOR_GRAY2BGR)[mask_map]

# saving .ply 
def write_ply(filename, verts, colors):
    verts = verts.reshape(-1, 3)
    colors = colors.reshape(-1, 3)
    with open(filename, 'w') as f:
        f.write('ply\nformat ascii 1.0\n')
        f.write(f'element vertex {len(verts)}\n')
        f.write('property float x\nproperty float y\nproperty float z\n')
        f.write('property uchar red\nproperty uchar green\nproperty uchar blue\n')
        f.write('end_header\n')
        for i in range(len(verts)):
            f.write(f'{verts[i][0]} {verts[i][1]} {verts[i][2]} {colors[i][0]} {colors[i][1]} {colors[i][2]}\n')

write_ply('output.ply', output_points, output_colors)

# disparity map showing
cv2.imshow('Disparity Map', (disparity_map - min_disp) / num_disp)
cv2.waitKey(0)
cv2.destroyAllWindows()
