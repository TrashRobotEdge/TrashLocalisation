# TrashLocalisation

A TurtleBot3 Burger + OAK-D Pro that **finds and approaches trash** (rung 1: Coca-Cola cans).
Autonomous Systems project (Université Côte d'Azur, G. Rocher). Edge AI counterpart: **[EdgeTrash](https://github.com/TrashRobotEdge/EdgeTrash)** (models, benchmark).

> **Status: Sprint 0 skeleton.** Packages are empty stubs. Nothing runs yet.
> Board: https://github.com/orgs/TrashRobotEdge/projects/1 · Plan: [docs/PROJECT_PLAN.md](docs/PROJECT_PLAN.md)

## Packages
| Package | Role | Build |
|---|---|---|
| `trash_description` | Our extensions of the professor's OAK-D Pro URDF + Gazebo can world | ament_cmake (data only) |
| `trash_detector` | Image → detections. Thin wrapper around EdgeTrash's `edgetrash` library, backend = ROS parameter | ament_python |
| `trash_localizer` | Detections + depth + camera_info → 3D target in `odom` (TF2) | ament_python |
| `trash_behaviour` | FSM (S1) → behaviour tree (S2), lidar safety stop | ament_python (BT library decided after 08/12) |
| `trash_bringup` | One-command launch (sim / real) | ament_python |

## Install (Ubuntu 22.04, ROS2 Humble, CycloneDDS)
1. Set up the host as in the [professor's README](https://github.com/gerald-rocher/Turtlebot3#readme) (ROS2 Humble, CycloneDDS, ROBOTIS packages, `gerald-rocher/Turtlebot3`).
2. Clone this repo next to it and build:
   ```bash
   cd ~/ros2_ws/src && git clone git@github.com:TrashRobotEdge/TrashLocalisation.git
   cd ~/ros2_ws && colcon build --symlink-install && source install/setup.bash
   ```

## Run
Not yet. See [DEMO.md](DEMO.md) (filled when the first loop works, S1).

## Docs
- [Architecture & interfaces](docs/architecture.md) · [Decisions (ADRs)](docs/decisions/) · [Problems log](docs/problems.md) · [Sprint journal](docs/journal/)
- [Contributing](CONTRIBUTING.md) · Report (LaTeX, assembled at the end from `docs/`): [report/](report/)
