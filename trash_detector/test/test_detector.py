"""Smoke test: a red box in an rgb8 Image goes through to_bgr -> hsv-red -> Detection2DArray."""

import numpy as np
from edgetrash import load_variant
from sensor_msgs.msg import Image
from trash_detector.detector_node import to_bgr, to_msg


def test_red_box_is_detected():
    rgb = np.zeros((480, 640, 3), np.uint8)
    rgb[200:300, 300:340] = (200, 0, 0)  # red in RGB order, as Gazebo sends it
    msg = Image(height=480, width=640, encoding="rgb8", step=640 * 3, data=rgb.tobytes())

    dets, _ = load_variant("hsv-red")(to_bgr(msg))
    out = to_msg(dets, msg.header)

    assert len(out.detections) == 1
    assert abs(out.detections[0].bbox.center.position.x - 320) < 2
