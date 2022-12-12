import os
from typing import List
import numpy as np
from skimage import filters, morphology
import roifile # Create ROI files compatible with ImageJ/FIJI

def median_filter(img: np.ndarray) -> np.ndarray:
        footprint = np.zeros((3, 3, 5, 5), dtype=np.uint8)
        footprint[1, 1] = morphology.disk(2)
        return filters.median(img, footprint)

def calculate_volume(channel: np.ndarray, voxel_size: List[float]):
        voxel_volume = np.prod(voxel_size)
        threshold = filters.threshold_otsu(channel[[0, -1], :, :])
        thresholded = (morphology.remove_small_objects(sl > threshold, min_size=16) for sl in channel)
        volume_slice = np.array([sl.sum() * voxel_volume for sl in thresholded])
        volume_total = volume_slice.sum()
        return volume_total, volume_slice

def make_rois(file: str, img: np.ndarray, germs: List[str]) -> None:
    roi_folder = r'D:\a_Projects\Ifey_Alio_\Data\ROI'
    roi_file_name = os.path.join(roi_folder , file.split('.tif')[0] + '.zip')
    if os.path.exists(roi_file_name):
            os.remove(roi_file_name)

    for ch, channel in enumerate(img):
            threshold = filters.threshold_otsu(channel[[0, -1], :, :])
            mask = np.array([morphology.remove_small_objects(sl > threshold, min_size=16) for sl in channel])
            for z, sl in enumerate(channel):
                    coords = np.argwhere(mask[z])[::2, ::-1]
                    if coords.shape[0]:
                            left, top = coords.min(axis=0)
                            right, bottom = coords.max(axis=0)
                            roi = roifile.ImagejRoi()
                            roi.version = 227
                            roi.roitype = roifile.ROI_TYPE(1)
                            roi.n_coordinates = coords.shape[0]
                            roi.coordinates = coords
                            roi.left = int(left)
                            roi.top = int(top)
                            roi.right = int(right)
                            roi.bottom = int(bottom)
                            roi.integer_coordinates = coords - [int(left), int(top)]
                            roi.c_position = ch + 1
                            roi.z_position =  z + 1
                            roi.t_position = 1
                            roi.arrow_style_or_aspect_ratio = 3
                            roi.name = germs[ch] + '_slice_' + str(z + 1)
                            roi.tofile(roi_file_name)

if __name__ == "__main__":
    pass