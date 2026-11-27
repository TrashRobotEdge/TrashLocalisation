# 0003: ROS interfaces between our nodes

- **Status:** accepted
- **Date:** 27/11/2026 · **Issue:** #3

## Context
Four people work on four nodes in parallel. They need a fixed contract. The sensor topics are fixed by the professor's OAK-D Pro model and bridge (`gerald-rocher/Turtlebot3` @ `cb2a91b`), checked in the running sim on 27/11.

## Options
1. Custom messages in our own interfaces package (as TurtleShot did).
2. Standard messages: `vision_msgs/Detection2DArray` for boxes, `geometry_msgs/PoseStamped` for the target.

## Decision
Option 2. Topics, types, frames and QoS as in [architecture.md](../architecture.md).

## Because
- Standard types work with RViz, `ros2 topic echo` and rosbag tools out of the box. One package less to build and explain.
- `Detection2DArray` already holds what we need (box, class, score, header). A custom message would copy it.
- Keeping the image header on detections lets #24 measure image → `cmd_vel` latency without extra fields.
- Reliable + keep last 1: newest data only, and it's what worked in our sim (best effort stalled, `problems.md`).

## Consequences
- `class_id` is a string. The baseline puts the class index there. Class names come with model A (#17).
- `/trash/target` is in the camera frame until #13. Whoever moves it to `odom` updates `trash_behaviour` in the same PR.
