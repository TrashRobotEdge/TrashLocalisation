# trash_description

The simulated world, and the launch file that puts the professor's TurtleBot3 Burger + OAK-D Pro in it.

**Run:** `ros2 launch trash_description sim.launch.py [world:=cans.sdf] [rviz:=true]` (or everything with `trash_bringup`).

- `worlds/cans.sdf`: the professor's empty world + one red cylinder (~33 cl can size) 1 m in front of the robot.
- `launch/sim.launch.py`: Gazebo (Fortress) with our world, then the professor's robot description and spawn launch files, reused as they are. Robot model `turtlebot3_burger_oak_d_pro`.

Out: everything the professor's bridge publishes (`rgb_camera/image`, `depth_camera/image`, `scan`, `odom`, `tf`, `clock`…), see `docs/architecture.md`.

**How to change it**
- New world: add an `.sdf` to `worlds/`, run with `world:=<file>`. Room, real cans, obstacles: #10.
- Our robot model (camera_info bridge, mount pose, depth noise): #8, #9. They add `urdf/` and our own bridge file here.
