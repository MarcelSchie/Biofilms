from functools import reduce
import numpy as np
from typing import Callable
from skimage import filters, morphology


ThresholdingMethod = Callable[[np.ndarray], np.ndarray]
ComposableFunction = Callable[[np.ndarray], np.ndarray]

def compose(*functions: ComposableFunction) -> ComposableFunction:
    return reduce(lambda f, g: lambda x: g(f(x)), functions)

def blur(sigma: float) -> ComposableFunction:
    def func(image: np.ndarray) -> np.ndarray:
        return np.array([filters.gaussian(slice, sigma=sigma) for slice in image])
    return func

def auto_li_thresholding(min_size: int=32, f_thr: float=2.0, verbose=False) -> ThresholdingMethod:
    def func(channel: np.ndarray) -> np.ndarray:
        step = int(channel.shape[0] / 5)
        imean = channel[::step].mean()
        threshold = filters.threshold_li(channel[::step])
        threshold = threshold * f_thr if threshold > imean * 1.5 else (threshold + imean) * f_thr
        if verbose:
            print((threshold))
        return np.array([morphology.remove_small_objects(slice > threshold, min_size=min_size) for slice in channel])
    return func

def manual_thresholding(threshold: float, min_size: int=32) -> ThresholdingMethod:
    def func(channel: np.ndarray) -> np.ndarray:
        return np.array([morphology.remove_small_objects(slice > threshold, min_size=min_size) for slice in channel])
    return func

def threshold(function: ThresholdingMethod) -> ComposableFunction:
    def func(channel: np.ndarray) -> np.ndarray:
        return function(channel)
    return func

if __name__ == "__main__":
    pass