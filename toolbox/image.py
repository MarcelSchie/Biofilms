import re
from typing import List, Tuple
import numpy as np
from skimage import io
from tifffile import TiffFile
from pathlib import Path
import difflib

#fluors_dict = {'mHoneyDew': 'eYFP', '1-ANS': 'Cyan', 'EGFP': 'EGFP', 'mCherry': 'mCherry', 'tdTomato': 'tdTomato', 'sfGFP': 'EGFP', 'Cyan': 'Cyan'}
fluors_dict = {'mHoneyDew': 'eYFP', 'EGFP': 'GFP', 'sfGFP': 'GFP', 'mCherry': 'mCherry', 'tdTomato': 'tdTomato', 'Cyan': 'Cyan', '1-ANS': 'Cyan'}

def load_image(path: Path) -> np.ndarray:
    # Load image
    img = io.imread(path)
    # Add extra dimension if image has only one channel
    if img.ndim == 3:
        img = np.expand_dims(img, axis=3)
    # Swap channel axis to first index
    img = np.moveaxis(img, np.argmin(img.shape), 0)
    return img

def find_strings_in_metadata(path: Path, string_to_find: str) -> List[str]:
    with TiffFile(path) as image:
        metadata = image.imagej_metadata['Info'].split('\n')
        return [line.split(' = ')[1] for line in metadata if line.startswith(string_to_find)]

def get_voxel_sizes(path: Path) -> List[float]:
    voxel_sizes = find_strings_in_metadata(path, r'Scaling|Distance|Value')
    voxel_sizes = list(map(float, voxel_sizes))
    return voxel_sizes

def get_fluors(path: Path) -> List[str]:
    return find_strings_in_metadata(path, r'Information|Image|Channel|Fluor')

def get_hours_post_infection(file: str) -> int:
    return re.findall("\d+h \w*", file)[-1].split(" ")[0]

def get_sample_number(file: str) -> int:
    return re.findall("\d+h \w*", file)[-1].split(" ")[1]

def get_crosstalk_fluor(path: Path) -> Tuple[int, str]:
    fluors = [fluors_dict[fluor] for fluor in get_fluors(path)]
    for channel, fluor in enumerate(fluors):
        if fluor in path.name:
            return channel, fluor
    return (0, '')

#def get_crosstalk_fluor(path: Path) -> Tuple[Dict[str, str], int]:
#    fluors = [fluors_dict[fluor] for fluor in get_fluors(path)]
#    for c, fluor in enumerate(fluors):
#        match = difflib.get_close_matches(fluor.lower(), path.name.lower().split(' '), n=1, cutoff=0.6)
#        if match:
#            return fluors_dict[fluor], c

if __name__ == "__main__":
    pass