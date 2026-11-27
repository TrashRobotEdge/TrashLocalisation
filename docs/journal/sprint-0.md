# Sprint 0: Define & de-risk (25/11 → 30/11)

## Goal
Everyone runs the sim · every device has run one inference · protocol steps 1–5 drafted · 2 model families chosen with reasons.

## Done
- 27/11, baseline loop in sim (#44, #3, #45–#49, [ADR 0004](../decisions/0004-baseline-scope.md)): `scripts/setup.sh` → one launch → detector → localiser → approach → stop.
- 27/11, dev VM measurements (VirtualBox, 4 vCPU, 12 GB, no 3D, code at `6400690`), with `ros2 launch trash_bringup sim.launch.py [variant:=hsv-red]` and small rclpy probes subscribed to our topics:

| What | `hsv-red` | `yolov8n-coco-640-fp32-onnx` |
|---|---|---|
| Gazebo real-time factor (`ign topic -e -t /world/default/stats -n 1`) | 0.24 | 0.28 |
| Detection messages (wall time) | 481 in 180 s, all with the can | 230 in 100 s (~2.3 Hz) |
| Detector `infer_ms` (node log) | 1–10 | 90–440 (104 p50 on an idle VM, EdgeTrash `results/summary.csv`) |
| Class given to the red cylinder | — | COCO 4 "airplane" (score 0.5–0.8), sometimes 41 "cup", 11 "stop sign" |
| Approach | stops with target z = 0.30 m, robot at x = 0.58 m (can at 1.0 m) | not measured |

- Localiser sanity check: target z + robot x stayed 0.88 m during the whole approach, i.e. the depth follows the robot's motion. Not ground truth: that's #12.

## Blocked / problems
- RTF ~0.25 on the dev VM (software rendering). Everyone: write your RTF in #1. See `problems.md`.

## Professor's answers (AS review 01/12, EAI review 02/12)

## Decisions taken (ADRs)
- 0001 Two repos, one ROS-free inference library
- 0002 ROS nodes run edgetrash from a venv
- 0003 ROS interfaces between our nodes
- 0004 A crude end-to-end baseline first
