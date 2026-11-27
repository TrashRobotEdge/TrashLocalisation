# Problems log

One entry per real problem. The professor grades the **diagnosis and alternatives**, not the absence of problems.

## Template
### YYYY-MM-DD: short title (issue #N)
- **Symptom:** what we saw
- **Diagnosis:** why it happens (evidence)
- **Alternatives:** options considered
- **Chosen:** what we did, because …

### 2026-11-27: `cv_bridge` breaks next to edgetrash (#44)
- **Symptom:** `CvBridge()` fails with `numpy.core.multiarray failed to import` in a Python that has EdgeTrash's `numpy==2.1.3`.
- **Diagnosis:** ROS Humble's apt OpenCV/`cv_bridge` are built for Ubuntu's numpy 1.21. `rclpy` and the message packages work with numpy 2 (tested).
- **Alternatives:** numpy 2 for all of ROS (`pip --user`) · loosen EdgeTrash's pin · a venv only our nodes use.
- **Chosen:** venv + no `cv_bridge` in our code, because it touches nothing else. [ADR 0002](decisions/0002-ros-python-env.md).

### 2026-11-27: `pip install -e EdgeTrash` fails in the venv (#44)
- **Symptom:** `build backend is missing the 'build_editable' hook`.
- **Diagnosis:** Ubuntu 22.04's pip 22.0.2. The same command works after upgrading pip to 26.3 (tested in a fresh venv). Likely cause, not verified: the old pip builds with Debian's setuptools 59, which has no editable hook.
- **Chosen:** `setup.sh` pins `pip==26.3` in the venv first.

### 2026-11-27: pytest can't start in the venv (#44)
- **Symptom:** `Plugin 'launch_testing' ... Argument(s) {'path'} are declared in the hookimpl but can not be found in the hookspec`, then the same for `launch_ros`.
- **Diagnosis:** the venv sees ROS Humble's pytest plugins, written for an older pytest than EdgeTrash's `pytest==9.2.0`.
- **Chosen:** `pytest.ini` disables those two plugins (we don't use launch tests).

### 2026-11-27: best-effort image subscribers stop after one frame (#46, #47)
- **Symptom:** in the launched loop, `trash_detector` processed one image (sometimes none) and then nothing, for minutes. The localiser's depth subscription did the same, so the robot used an old depth image and hit the can.
- **Diagnosis:** the process was idle in `rclpy` waiting for messages (stack via `PYTHONFAULTHANDLER=1` + `kill -ABRT`), while other subscribers still got images at ~1.5 Hz. The QoS was compatible (`ros2 topic info -v`). Root cause not found. Hypothesis: 900 KB images are split into many UDP fragments, and a best-effort reader drops the whole frame when one fragment is lost, which is likely with Gazebo using all CPUs.
- **Alternatives:** reliable keep-last-1 · bigger CycloneDDS socket buffers (`cyclonedds.xml`, #27) · smaller images.
- **Chosen:** reliable keep-last-1 for every subscription, because it's one line and still gives the newest frame. Result: 481 detection messages in 3 min, every one with the can. Worth revisiting with #27.

### 2026-11-27: `camera_info` is not bridged (#8)
- **Symptom:** no intrinsics on any ROS topic.
- **Diagnosis:** Gazebo publishes `/rgb_camera/camera_info` and `/depth_camera/camera_info` (`ign topic -l`), the professor's `turtlebot3_bridge.yaml` maps `camera/camera_info`.
- **Chosen (baseline):** intrinsics from the HFOV param. Proper fix: our own bridge file, #8.

### 2026-11-27: Gazebo at ~0.25× real time on the dev VM (#1)
- **Symptom:** real-time factor 0.24–0.28 with the full loop, camera at ~1.5 frames/s wall time.
- **Diagnosis:** VirtualBox gives no 3D acceleration (`VMware: No 3D enabled`), OpenGL is `llvmpipe` (software). Two cameras + a GPU lidar are rendered on the CPU.
- **Alternatives:** enable 3D acceleration in VirtualBox · native/dual-boot Ubuntu · lower camera rate/resolution in the sim.
- **Chosen:** none yet. The loop still works, just slowly. Everyone reports their RTF in #1, then we decide.
