import difflib
from enum import Enum
from pathlib import Path
import os
from typing import List, Tuple
import numpy as np

class Culture(Enum):
    PAO1 = 'PAO1'
    K279A = 'K279a'
    SAUREUS = 'Aureus'
    CALBICANS = 'Albicans'

fluors_to_color = {'eYFP': 'orange', 'Cyan': 'blue', '1-ANS': 'blue', 'EGFP' : 'green', 'mCherry' : 'red', 'tdTomato' : 'red', 'ATTO 425' : 'blue', 'mHoneyDew': 'orange'}

def get_all_tiffs_in(folder: Path) -> List[str]:
    return [file for file in os.listdir(folder) if file.endswith(".tif")]

def get_germs(file: str) -> List[str]:
    germs = []
    for culture in Culture:
        match = difflib.get_close_matches(culture.name.lower(), file.lower().split(' '), n=1, cutoff=0.6)
        if match:
            germs.append(match[0])
    return germs

def get_germs_new(file: str, colors: List[str], verbose: bool=False) -> Tuple[List[str], List[str]]:
    cultures = ['PAO1', 'K279a', 'Aureus', 'Albicans']
    germs_ = []
    fluors_ = []
    for part in file.split('+'):
        for culture in cultures:
            match = difflib.get_close_matches(culture.lower(), part.lower().split(' '), n=1, cutoff=0.6)
            if match:
                germs_.append(culture)
        for fluor in list(fluors_to_color.keys()):
            match = difflib.get_close_matches(fluor.lower(), part.lower().split(' '), n=1, cutoff=0.6)
            if match:
                fluors_.append(fluor)
                break
    colors_ = [fluors_to_color[fluor] for fluor in fluors_]
    
    idx = []
    for color in colors:
        idx.append(np.argwhere(np.array(colors_) == color)[0][0])
    if verbose:
        print(germs_, fluors_, colors_, idx)
    return [germs_[i].lower() for i in idx], germs_

if __name__ == "__main__":
    pass