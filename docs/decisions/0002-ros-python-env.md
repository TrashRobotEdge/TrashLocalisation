# 0002: ROS nodes run edgetrash from a venv with system packages

- **Status:** accepted
- **Date:** 27/11/2026 · **Issue:** #44

## Context
`trash_detector` imports `edgetrash` (ADR 0001). EdgeTrash pins `numpy==2.1.3` and its own OpenCV. ROS Humble's apt packages are built for Ubuntu 22.04's numpy 1.21: tested on 27/11, `CvBridge()` fails with numpy 2 (`numpy.core.multiarray failed to import`). `rclpy` + `sensor_msgs` work fine with numpy 2 (also tested).

## Options
1. `pip install --user edgetrash`: numpy 2 lands under **every** ROS python tool (cv_bridge, rqt plots…).
2. Loosen EdgeTrash to numpy 1: another team's pins, and its TensorFlow export needs numpy 2.
3. A venv with `--system-site-packages` (sees rclpy and the msgs) + edgetrash, and build with `python -m colcon build` from inside it, so colcon runs under the venv's python and writes it into our nodes' shebang.

## Decision
Option 3, venv at `~/ros2_ws/.venv`, made by `scripts/setup.sh`. Our nodes don't use `cv_bridge`: images are read with `np.frombuffer`.

## Because
- numpy 2 only reaches our nodes: their shebang is the venv's python, the rest of ROS keeps `/usr/bin/python3`.
- Nothing to activate at run time, one build command.
- No change to EdgeTrash's pins.

## Consequences
- Plain `colcon build` (system python) would give our nodes the wrong shebang. Always `python -m colcon build` with the venv active (README).
- No `cv_bridge` in our code.
