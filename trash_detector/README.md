# trash_detector

Camera image → `edgetrash` → boxes. All detection code lives in EdgeTrash (ADR 0001); this node only converts ROS messages.

**Run:** started by `trash_bringup`. Alone: `ros2 run trash_detector detector --ros-args --params-file config/detector.yaml -p variant:=hsv-red`

| In | Out |
|---|---|
| `rgb_camera/image` (rgb8 or bgr8) | `/trash/detections` (`Detection2DArray`, same header as the image) |

Logs every 2 s: number of detections and `pre_ms` / `infer_ms` / `post_ms`.

**How to change it**
- Model: launch argument `variant:=<name>`, names in EdgeTrash `models/manifest.yaml`. A new model = a manifest entry + its file in EdgeTrash `models/files/` (#17).
- Score threshold, topics: `config/detector.yaml`.
- HSV thresholds: `backend_opts` of `hsv-red` in the EdgeTrash manifest (#11).
- No `cv_bridge` here: images are read with numpy (ADR 0002).
