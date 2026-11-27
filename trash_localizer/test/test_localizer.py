"""Smoke test: a box on a flat 1.5 m depth image gives a point 1.5 m ahead."""

import math

import numpy as np
from trash_localizer.localizer_node import box_to_point


def test_box_at_image_centre_is_straight_ahead():
    depth = np.full((480, 640), 1.5, np.float32)
    depth[0, 0] = np.inf  # invalid pixels must be ignored

    x, y, z = box_to_point((320, 240, 40, 60), depth, hfov=1.047)

    assert math.isclose(z, 1.5)
    assert abs(x) < 1e-6 and abs(y) < 1e-6
