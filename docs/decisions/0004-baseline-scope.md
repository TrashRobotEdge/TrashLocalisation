# 0004: A crude end-to-end baseline first, then everyone improves one piece

- **Status:** accepted
- **Date:** 27/11/2026 · **Issues:** #44, #3, #45–#49

## Context
After S0 the packages were empty, and every S1 issue depended on another one (no world → no detector test → no localiser test → …). One of us has time now and less later in the semester.

## Options
1. Build piece by piece as planned, each issue waiting on the previous one.
2. One person wires the whole loop in its simplest form, then the issues become "improve X" on a running system.

## Decision
Option 2. The baseline is plumbing: one command, every node exists and talks to the next, each piece is the dumbest thing that works. Graded work (URDF, world, FSM, BT, TF2, Nav2) stays in the issues.

## Because
- Nobody waits: every issue can be tested in the full loop from day one.
- Integration problems show up now, not in S3 (it already found four: `problems.md`, 27/11).
- The issues stay real work, each with a lecture behind it.

## What's crude on purpose → who fixes it

| Piece | Baseline | Improved in |
|---|---|---|
| World | Empty world + one red cylinder 1 m ahead | #10 |
| Camera intrinsics | From the HFOV param | #8 (`camera_info`) |
| Sim camera | Professor's mount pose, no depth noise | #9 |
| Detector | COCO yolov8n (no can class: calls the cylinder "airplane"), or `hsv-red` with default thresholds | #17 (model A), #11 (HSV tuning) |
| Localiser | Median depth in the box, camera frame, accuracy not measured | #12 (accuracy + frames), #13 (`odom`) |
| Behaviour | One P-controller, implicit states | #15 (FSM), #18–#19 (BT), #20 (Braitenberg) |
| Safety | Lidar front cone, untested against obstacles | #16 |
| DDS | Defaults, reliable keep-last-1 | #27 (`cyclonedds.xml`, deadline) |

## Consequences
- Changing a piece = change its node or YAML, rerun `ros2 launch trash_bringup sim.launch.py`. Each package README says where.
- Measured on the dev VM (27/11, `variant:=hsv-red`): the robot approaches the cylinder and stops with the target at 0.30 m (`stop_dist`). Logged in `docs/journal/sprint-0.md`.
