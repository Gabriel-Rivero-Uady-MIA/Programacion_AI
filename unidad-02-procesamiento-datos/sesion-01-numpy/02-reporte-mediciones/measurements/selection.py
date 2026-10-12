import numpy as np
import numpy.typing as npt

from measurements.processing import validate_shape

type FloatArray = npt.NDArray[np.float64]


def select_warm_rounds(readings: FloatArray, threshold: float) -> FloatArray:

    validate_shape(readings)
    if not np.isfinite(readings).all():
        raise ValueError("Function requires finite readings")
    if not np.isfinite(threshold):
        raise ValueError("threshold must be finite")
    north_readings = readings[:, 0]
    warm = north_readings >= threshold
    selected_warm = readings[warm]

    return selected_warm
