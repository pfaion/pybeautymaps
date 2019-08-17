import pytest

from pybeautymaps import utils

VALID_LATLON = (37.030347, -93.473126)
VALID_SIZE = 1.2

def test_bbox_from_centered_raise_negative_size():
    with pytest.raises(ValueError):
        utils.bbox_from_centered(VALID_LATLON, -1)
    
def test_bbox_from_centered_raise_wrong_latlon():
    with pytest.raises(ValueError):
        utils.bbox_from_centered((-100, 0), VALID_SIZE)
    with pytest.raises(ValueError):
        utils.bbox_from_centered((100, 0), VALID_SIZE)
    with pytest.raises(ValueError):
        utils.bbox_from_centered((0, -200), VALID_SIZE)
    with pytest.raises(ValueError):
        utils.bbox_from_centered((0, 200), VALID_SIZE)
