from typing import List
import numpy as np
from skimage import filters

def calculate_crosstalk(img: np.ndarray, main_channel: int) -> List[float]:
    thr = filters.threshold_otsu(img[main_channel])
    crosstalk = [0, 0, 0]
    for ch in {0, 1, 2} - {main_channel}:
        cr = np.divide(img[ch], img[main_channel], out=np.zeros_like(img[main_channel], dtype=np.float16), where=img[main_channel] > thr)
        vals, bins = np.histogram(cr[cr > 0].flatten(), range=(0, 1), bins=100)
        imax = np.argmax(vals)
        crosstalk[ch] = (bins[imax + 1] + bins[imax]) / 2
    return crosstalk

def correct_crosstalk_old(img, colors, germs, crosstalk, n_colors=2**16-1):
    cmp = np.zeros_like(img)
    for ch, color in enumerate(colors):
        for germ in germs:
            if color in crosstalk[germ]['crosstalk']:
                cmp[ch] += (img[ch] * crosstalk[germ]['crosstalk'][color]).astype(np.uint16)
    return np.clip(img - cmp, 0, n_colors)

def correct_crosstalk(img, germs, colors, crosstalk, n_colors=2**16 - 1):
    cmp = np.zeros_like(img)
    for germ in germs:
        for channel, color in enumerate(colors):
            if color =='orange':
                color = 'blue'
            cmp[channel] += (img[channel] * crosstalk.loc[crosstalk.germ == germ][color].values[0]).astype(np.uint16)
    return np.clip(img - cmp, 0, 2**16 - 1)

if __name__ == "__main__":
    pass