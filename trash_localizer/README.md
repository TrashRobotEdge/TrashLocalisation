# trash_localizer

Best detection + depth image → where the can is, in metres.

**Run:** started by `trash_bringup`. Alone: `ros2 run trash_localizer localizer --ros-args --params-file config/localizer.yaml`

| In | Out |
|---|---|
| `/trash/detections`, `depth_camera/image` (32FC1, m) | `/trash/target` (`PoseStamped`, depth optical frame: x right, y down, z forward) |

How: highest-score box above `min_score` → median of the valid depth pixels in the box → back-projected with focal length `f = (width/2) / tan(hfov/2)`. Uses the latest depth image, no time sync.

**How to change it**
- Values, topics: `config/localizer.yaml`.
- Real intrinsics from `camera_info` instead of `hfov`: #8. Accuracy check and frame question: #12. Target in `odom` with TF2: #13 (update `trash_behaviour` too).
- The maths is in `box_to_point()`, tested in `test/test_localizer.py`.
