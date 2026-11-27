# trash_behaviour

Drives the robot to the target and stops. The lidar stop overrides everything.

**Run:** started by `trash_bringup`. Alone: `ros2 run trash_behaviour approach --ros-args --params-file config/approach.yaml`

| In | Out |
|---|---|
| `/trash/target` (camera frame), `scan` | `cmd_vel` |

Baseline logic, every `1/rate` s (`command()` in `approach_node.py`):
- no target for `target_timeout` s → turn on the spot (search);
- else turn towards it (`k_turn`) and drive (`k_drive`, max `max_drive`) until it is `stop_dist` away;
- anything closer than `safety_dist` in the lidar front cone → no forward motion. The lidar is ~0.18 m high, so it doesn't see cans.

**How to change it**
- Speeds, distances, topics: `config/approach.yaml`.
- Real states: FSM (#15), then behaviour tree (#18, #19), Braitenberg controller (#20). Keep `command()`'s inputs/outputs, so the launch doesn't change.
- Safety tuning and obstacle tests: #16.
