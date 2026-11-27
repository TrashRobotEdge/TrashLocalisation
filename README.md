# TrashLocalisation

A TurtleBot3 Burger + OAK-D Pro that **finds and approaches trash** (rung 1: Coca-Cola cans).
Autonomous Systems project (Université Côte d'Azur, G. Rocher). Edge AI counterpart: **[EdgeTrash](https://github.com/TrashRobotEdge/EdgeTrash)** (models, benchmark).

> **Status: baseline.** The whole loop runs in sim, crude on purpose ([ADR 0004](docs/decisions/0004-baseline-scope.md)): each issue improves one piece.
> Board: https://github.com/orgs/TrashRobotEdge/projects/1 · Plan: [docs/PROJECT_PLAN.md](docs/PROJECT_PLAN.md)

## Packages
| Package | Role | Build |
|---|---|---|
| `trash_description` | Gazebo can world + sim launch (our URDF extensions come in #8, #9) | ament_cmake (data only) |
| `trash_detector` | Image → detections. Thin wrapper around EdgeTrash's `edgetrash` library, model = `variant` | ament_python |
| `trash_localizer` | Best detection + depth → 3D target (camera frame; `odom` in #13) | ament_python |
| `trash_behaviour` | Approach + lidar stop (P-controller → FSM #15 → BT #18) | ament_python |
| `trash_bringup` | One-command launch (sim; real robot later) | ament_python |

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
```bash
ros2 launch trash_bringup sim.launch.py                    # NN: yolov8n COCO (no can class yet)
ros2 launch trash_bringup sim.launch.py variant:=hsv-red   # colour threshold: drives to the red can
```
Arguments: `variant` (EdgeTrash `models/manifest.yaml`), `world` (file in `trash_description/worlds`), `rviz:=true`. What you should see: [DEMO.md](DEMO.md).

Tests and lint (with the workspace sourced): `~/ros2_ws/.venv/bin/python -m pytest` · `pre-commit run --all-files`.

## Docs
- [Architecture & interfaces](docs/architecture.md) · [Decisions (ADRs)](docs/decisions/) · [Problems log](docs/problems.md) · [Sprint journal](docs/journal/)
- [Contributing](CONTRIBUTING.md) · Report (LaTeX, assembled at the end from `docs/`): [report/](report/)
