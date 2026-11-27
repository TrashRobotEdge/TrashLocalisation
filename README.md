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
1. ROS2 Humble ([professor's README](https://github.com/gerald-rocher/Turtlebot3#readme), "Install ROS2 Humble") and `gh auth login`.
2. Clone and run the setup script (asks for sudo once, for apt):
   ```bash
   mkdir -p ~/ros2_ws/src && cd ~/ros2_ws/src && gh repo clone TrashRobotEdge/TrashLocalisation
   TrashLocalisation/scripts/setup.sh   # then open a new shell
   ```

`scripts/setup.sh` does the rest of the professor's setup and is safe to re-run:
- apt: Gazebo Fortress bridge, Nav2, Cartographer, CycloneDDS, `vision_msgs`
- ROBOTIS repos + `gerald-rocher/Turtlebot3` at pinned commits (in the script)
- EdgeTrash at a pinned commit (`~/EdgeTrash`, or set `EDGETRASH_DIR`), installed in the venv `~/ros2_ws/.venv`, model from the `models-v1` release, checksum checked
- `python -m colcon build`, pre-commit hooks, `~/.bashrc` lines

**Why a venv:** EdgeTrash needs numpy 2, the apt `cv_bridge`/OpenCV need numpy 1 ([ADR 0002](docs/decisions/0002-ros-python-env.md)). Our nodes get the venv's python through their shebang, nothing to activate. After changing a `package.xml` or `setup.py`: `cd ~/ros2_ws && source .venv/bin/activate && python -m colcon build --symlink-install`.

## Run
Not yet. See [DEMO.md](DEMO.md) (filled when the first loop works, S1).

## Docs
- [Architecture & interfaces](docs/architecture.md) · [Decisions (ADRs)](docs/decisions/) · [Problems log](docs/problems.md) · [Sprint journal](docs/journal/)
- [Contributing](CONTRIBUTING.md) · Report (LaTeX, assembled at the end from `docs/`): [report/](report/)
