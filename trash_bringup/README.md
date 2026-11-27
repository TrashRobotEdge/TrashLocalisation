# trash_bringup

One command for the whole system.

```bash
ros2 launch trash_bringup sim.launch.py [variant:=hsv-red] [world:=cans.sdf] [rviz:=true]
```

Starts `trash_description`'s sim, then `trash_detector`, `trash_localizer` and `trash_behaviour`, each with its `config/*.yaml` and sim time.

**How to change it**
- Node settings belong in each package's YAML, not here. Only switches are launch arguments (`variant`, `world`, `rviz`).
- Real robot launch: #34, #35. `cyclonedds.xml` and a `behaviour` (fsm/bt) argument: #27.
