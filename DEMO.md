# Demo instructions

> Baseline version (27/11). To be tested by someone who didn't write it (#28).

## 1. Simulation (guaranteed)
After [Install](README.md#install-ubuntu-2204-ros2-humble-cyclonedds), in a new shell:
```bash
ros2 launch trash_bringup sim.launch.py variant:=hsv-red
```
What you should see:
- Gazebo opens: the robot at the origin, a red cylinder ("can") 1 m ahead. The first start downloads the ground and sun models (internet needed once).
- The robot turns on the spot until the can is in view, drives to it and stops ~0.3 m in front (camera to can).
- `[trash_detector]` logs every 2 s: number of detections + pre/infer/post times in ms.
- On our dev VM (software rendering) it takes ~2 min wall time: Gazebo runs at ~0.25× real time.

With the NN (default `variant`, COCO yolov8n): same, but it has no can class. It calls the cylinder "airplane" (COCO 4) and still drives to it, because the localiser takes the best box of any class (#17 fixes that).

Useful checks:
```bash
ros2 topic echo /trash/target --field pose.position   # z = distance ahead (m)
ign topic -e -t /world/default/stats -n 1 | grep real_time_factor
```
If `ros2 topic list/echo` hangs or says "!rclpy.ok()": `ros2 daemon stop`, then retry.

## 2. Real robot (if the chassis is ready)
TODO (#34, #35): power-on order, network/DDS setup, launch command, safety (how to stop the robot).

## 3. Backup
TODO (#29): link to the demo videos (sim + real).
