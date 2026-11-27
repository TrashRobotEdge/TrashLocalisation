"""Baseline behaviour (ADR 0004): search -> turn to the target and drive -> stop. Lidar stop overrides.

One P-controller with implicit states. The real FSM is #15, the behaviour tree #18-#19.
Target in the camera optical frame (x right, z forward) until #13 moves it to odom.
"""

import math

import numpy as np
import rclpy
from geometry_msgs.msg import PoseStamped, Twist
from rclpy.node import Node
from sensor_msgs.msg import LaserScan

GAINS = ("search_turn", "k_turn", "k_drive", "max_drive", "stop_dist", "safety_dist")


def front_min(scan: LaserScan, cone: float) -> float:
    """Closest valid lidar range within +-cone rad of straight ahead (angle 0), inf if none."""
    r = np.asarray(scan.ranges, dtype=float)
    a = scan.angle_min + np.arange(len(r)) * scan.angle_increment
    a = (a + math.pi) % (2 * math.pi) - math.pi  # this lidar scans 0..2pi, so wrap to -pi..pi
    ok = np.isfinite(r) & (r >= scan.range_min) & (np.abs(a) <= cone)
    return float(r[ok].min()) if ok.any() else math.inf


def command(target, ahead: float, p: dict) -> tuple[float, float]:
    """target = (x, z) in metres or None, ahead = front_min() -> (linear m/s, angular rad/s)."""
    if target is None:
        return 0.0, p["search_turn"]  # search: turn on the spot
    x, z = target
    angular = -p["k_turn"] * math.atan2(x, z)  # target on the right (x > 0) -> turn right (negative z)
    linear = min(max(p["k_drive"] * (z - p["stop_dist"]), 0.0), p["max_drive"])
    if ahead < p["safety_dist"]:
        linear = 0.0  # safety stop wins over everything
    return linear, angular


class ApproachNode(Node):
    def __init__(self):
        super().__init__("trash_behaviour", automatically_declare_parameters_from_overrides=True)
        self.p = {name: self.param(name) for name in GAINS}
        self.cone = self.param("front_cone")
        self.timeout = self.param("target_timeout")
        self.target, self.target_time, self.ahead = None, None, math.inf
        self.pub = self.create_publisher(Twist, self.param("cmd_vel_topic"), 1)
        self.create_subscription(PoseStamped, self.param("target_topic"), self.on_target, 1)
        self.create_subscription(LaserScan, self.param("scan_topic"), self.on_scan, 1)
        self.create_timer(1.0 / self.param("rate"), self.tick)

    def param(self, name):
        return self.get_parameter(name).value  # raises if config/approach.yaml lacks it

    def on_target(self, msg: PoseStamped):
        self.target = (msg.pose.position.x, msg.pose.position.z)
        self.target_time = self.get_clock().now()

    def on_scan(self, msg: LaserScan):
        self.ahead = front_min(msg, self.cone)

    def tick(self):
        fresh = self.target_time is not None and (self.get_clock().now() - self.target_time).nanoseconds < self.timeout * 1e9
        linear, angular = command(self.target if fresh else None, self.ahead, self.p)
        cmd = Twist()
        cmd.linear.x, cmd.angular.z = linear, angular
        self.pub.publish(cmd)


def main():
    rclpy.init()
    node = ApproachNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.pub.publish(Twist())  # leave the robot stopped
        node.destroy_node()
        rclpy.try_shutdown()
