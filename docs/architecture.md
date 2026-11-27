# Architecture & interfaces

Decided in [ADR 0003](decisions/0003-ros-interfaces.md). Baseline state: [ADR 0004](decisions/0004-baseline-scope.md).

```
Gazebo (professor's TB3 + OAK-D Pro) ─ rgb_camera/image ─► trash_detector ─ /trash/detections ─► trash_localizer ─ /trash/target ─► trash_behaviour ─► cmd_vel
                                      ─ depth_camera/image ──────────────────────────────────────►        ▲                                 ▲
                                      ─ scan ──────────────────────────────────────────────────────────────────────────────────────────────┘
```

| Topic | Type | From → To | Notes |
|---|---|---|---|
| `rgb_camera/image` | `sensor_msgs/Image`, rgb8 640×480 | Gazebo bridge → detector | frame `oak_d_pro_color_optical_frame` |
| `depth_camera/image` | `sensor_msgs/Image`, 32FC1 metres | Gazebo bridge → localiser | frame `oak_d_pro_depth_optical_frame`, inf where nothing is in range |
| `scan` | `sensor_msgs/LaserScan`, 360 beams, 0→2π | Gazebo bridge → behaviour | plane ~0.18 m high: doesn't see cans |
| `/trash/detections` | `vision_msgs/Detection2DArray` | detector → localiser | header = the image's (for latency, #24). `class_id` = class index of the variant |
| `/trash/target` | `geometry_msgs/PoseStamped` | localiser → behaviour | depth optical frame (x right, y down, z forward). `odom` after #13 |
| `cmd_vel` | `geometry_msgs/Twist` | behaviour → Gazebo bridge | |

- **QoS:** every subscription is reliable, keep last 1: the newest message, no stale queue. Not best effort: see `problems.md` (27/11). Deadline QoS: #27.
- **Frames:** TF from the professor's URDF. Whether the two optical frames are oriented right is open (#12). Nothing in the baseline uses TF.
- **Not bridged yet:** `camera_info`. Gazebo publishes `rgb_camera/camera_info` and `depth_camera/camera_info`, the professor's bridge maps `camera/camera_info` (#8).

Computation graph figure: #30.
