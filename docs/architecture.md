# Architecture & interfaces

> To be frozen in issue #3 (S0). Until then this is the **proposal** from the plan.

```
OAK-D Pro (RGB+depth) ─► trash_detector ─Detection2DArray─► trash_localizer ─PoseStamped(odom)─► trash_behaviour ─► cmd_vel
                         backend ∈ {hsv | onnx | tflite | hailo | oak}   ▲ depth + camera_info + TF2           ▲ /scan safety stop
```

| Topic | Type | From → To | QoS |
|---|---|---|---|
| `rgb_camera/image` | `sensor_msgs/Image` | camera → detector | sensor_data, depth 1 |
| `depth_camera/image` | `sensor_msgs/Image` | camera → localizer | sensor_data, depth 1 |
| `camera_info` (to add in sim) | `sensor_msgs/CameraInfo` | camera → localizer | |
| `/trash/detections` | `vision_msgs/Detection2DArray` | detector → localizer | reliable + deadline |
| `/trash/target` | `geometry_msgs/PoseStamped` (`odom`) | localizer → behaviour | reliable |
| `/cmd_vel` | `geometry_msgs/Twist` | behaviour → base | |

Frames: TODO (from the URDF TF tree). Computation graph figure: TODO (`rqt_graph`, S3).
