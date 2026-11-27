"""Camera image -> edgetrash detector -> /trash/detections.

All values come from config/detector.yaml (no defaults in code, so there is one place to change them).
"""

import cv2
import numpy as np
import rclpy
from edgetrash import load_variant
from rclpy.node import Node
from sensor_msgs.msg import Image
from vision_msgs.msg import Detection2D, Detection2DArray, ObjectHypothesisWithPose


def to_bgr(msg: Image) -> np.ndarray:
    """rgb8/bgr8 Image -> BGR array (what edgetrash expects). No cv_bridge: numpy 2 clash, ADR 0002."""
    if msg.encoding not in ("rgb8", "bgr8"):
        raise ValueError(f"unsupported encoding {msg.encoding!r}")
    rows = np.frombuffer(msg.data, np.uint8).reshape(msg.height, msg.step)  # step may include padding
    img = rows[:, : msg.width * 3].reshape(msg.height, msg.width, 3)
    return cv2.cvtColor(img, cv2.COLOR_RGB2BGR) if msg.encoding == "rgb8" else img.copy()


def to_msg(dets, header) -> Detection2DArray:
    """edgetrash detections (x0 y0 x1 y1 in pixels) -> Detection2DArray with the image's header."""
    out = Detection2DArray(header=header)
    for d in dets:
        x0, y0, x1, y1 = d.box
        det = Detection2D(header=header)
        det.bbox.center.position.x = (x0 + x1) / 2
        det.bbox.center.position.y = (y0 + y1) / 2
        det.bbox.size_x = x1 - x0
        det.bbox.size_y = y1 - y0
        hyp = ObjectHypothesisWithPose()
        hyp.hypothesis.class_id = str(d.cls)  # class index of the variant (COCO for the baseline model)
        hyp.hypothesis.score = d.score
        det.results.append(hyp)
        out.detections.append(det)
    return out


class DetectorNode(Node):
    def __init__(self):
        super().__init__("trash_detector", automatically_declare_parameters_from_overrides=True)
        variant = self.param("variant")
        self.detector = load_variant(variant, conf=self.param("conf"))
        self.pub = self.create_publisher(Detection2DArray, self.param("detections_topic"), 1)
        # QoS 1 = reliable, keep only the newest frame. Not best effort: best-effort image
        # subscribers stopped after one frame in our sim (problems.md).
        self.create_subscription(Image, self.param("image_topic"), self.on_image, 1)
        self.get_logger().info(f"loaded variant {variant}")

    def param(self, name):
        return self.get_parameter(name).value  # raises if config/detector.yaml lacks it

    def on_image(self, msg: Image):
        dets, ms = self.detector(to_bgr(msg))
        self.pub.publish(to_msg(dets, msg.header))
        timings = " ".join(f"{k}={v:.1f}" for k, v in ms.items())
        self.get_logger().info(f"{len(dets)} detections, {timings}", throttle_duration_sec=2.0)


def main():
    rclpy.init()
    node = DetectorNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.try_shutdown()
