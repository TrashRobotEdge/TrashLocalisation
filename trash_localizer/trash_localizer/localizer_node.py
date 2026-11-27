"""Best detection + depth image -> /trash/target, a 3D point in the camera's optical frame.

Baseline (ADR 0004): intrinsics from the HFOV param, not camera_info (#8), no TF to odom yet (#13).
Optical convention: x right, y down, z forward, metres.
"""

import math

import numpy as np
import rclpy
from geometry_msgs.msg import PoseStamped
from rclpy.node import Node
from sensor_msgs.msg import Image
from vision_msgs.msg import Detection2DArray


def depth_to_array(msg: Image) -> np.ndarray:
    """32FC1 depth Image (metres) -> float32 array. No cv_bridge: ADR 0002."""
    if msg.encoding != "32FC1":
        raise ValueError(f"unsupported depth encoding {msg.encoding!r}")
    rows = np.frombuffer(msg.data, np.float32).reshape(msg.height, msg.step // 4)
    return rows[:, : msg.width]


def box_to_point(box, depth: np.ndarray, hfov: float):
    """Box (cx, cy, w, h in pixels) -> (x, y, z) in metres, or None if the box has no valid depth.

    Pinhole camera with square pixels, principal point at the image centre: true in Gazebo.
    """
    h, w = depth.shape
    f = (w / 2) / math.tan(hfov / 2)
    cx, cy, bw, bh = box
    x0, x1 = int(max(cx - bw / 2, 0)), int(min(cx + bw / 2, w))
    y0, y1 = int(max(cy - bh / 2, 0)), int(min(cy + bh / 2, h))
    patch = depth[y0:y1, x0:x1]
    patch = patch[np.isfinite(patch)]  # Gazebo gives inf/nan where nothing is in range
    if patch.size == 0:
        return None
    z = float(np.median(patch))  # median: the box also covers some background
    return (cx - w / 2) * z / f, (cy - h / 2) * z / f, z


class LocalizerNode(Node):
    def __init__(self):
        super().__init__("trash_localizer", automatically_declare_parameters_from_overrides=True)
        self.hfov = self.param("hfov")
        self.min_score = self.param("min_score")
        self.depth = None
        self.pub = self.create_publisher(PoseStamped, self.param("target_topic"), 1)
        self.create_subscription(Image, self.param("depth_topic"), self.on_depth, 1)  # reliable, newest only
        self.create_subscription(Detection2DArray, self.param("detections_topic"), self.on_detections, 1)

    def param(self, name):
        return self.get_parameter(name).value  # raises if config/localizer.yaml lacks it

    def on_depth(self, msg: Image):
        self.depth = msg  # keep only the latest; converted when a detection needs it

    def on_detections(self, msg: Detection2DArray):
        if self.depth is None:
            return
        scored = [(d.results[0].hypothesis.score, d) for d in msg.detections if d.results]
        scored = [(s, d) for s, d in scored if s >= self.min_score]
        if not scored:
            return
        best = max(scored, key=lambda sd: sd[0])[1]
        b = best.bbox
        point = box_to_point((b.center.position.x, b.center.position.y, b.size_x, b.size_y), depth_to_array(self.depth), self.hfov)
        if point is None:
            return
        target = PoseStamped()
        target.header.stamp = msg.header.stamp  # image time, kept for the latency measure (#24)
        target.header.frame_id = self.depth.header.frame_id
        target.pose.position.x, target.pose.position.y, target.pose.position.z = point
        target.pose.orientation.w = 1.0
        self.pub.publish(target)


def main():
    rclpy.init()
    node = LocalizerNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.try_shutdown()
