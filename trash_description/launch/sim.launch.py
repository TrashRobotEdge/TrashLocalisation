"""Gazebo with our world + the professor's TurtleBot3 Burger + OAK-D Pro.

Same as his projects_empty_world.launch.py, but the world is an argument.
Robot description and spawn are his launch files, reused as they are.
"""

import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import AppendEnvironmentVariable, DeclareLaunchArgument, IncludeLaunchDescription, SetEnvironmentVariable
from launch.conditions import IfCondition
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution
from launch_ros.actions import Node


def generate_launch_description():
    ours = get_package_share_directory("trash_description")
    tb3_gazebo = get_package_share_directory("turtlebot3_gazebo")
    projects = os.path.join(tb3_gazebo, "launch", "projects")
    gz_sim = os.path.join(get_package_share_directory("ros_gz_sim"), "launch", "gz_sim.launch.py")

    world = LaunchConfiguration("world")
    rviz = LaunchConfiguration("rviz")

    return LaunchDescription(
        [
            DeclareLaunchArgument("world", default_value="cans.sdf", description="file in trash_description/worlds"),
            DeclareLaunchArgument("rviz", default_value="false"),
            # His launch files read the robot model from this variable.
            SetEnvironmentVariable("PROJECT_MODEL", "turtlebot3_burger_oak_d_pro"),
            AppendEnvironmentVariable("GZ_SIM_RESOURCE_PATH", os.path.join(tb3_gazebo, "models")),
            IncludeLaunchDescription(
                PythonLaunchDescriptionSource(gz_sim),
                launch_arguments={
                    "gz_args": ["-r -s -v2 ", PathJoinSubstitution([ours, "worlds", world])],
                    "on_exit_shutdown": "true",
                }.items(),
            ),
            IncludeLaunchDescription(PythonLaunchDescriptionSource(gz_sim), launch_arguments={"gz_args": "-g -v2"}.items()),
            IncludeLaunchDescription(
                PythonLaunchDescriptionSource(os.path.join(projects, "projects_robot_state_publisher.launch.py")),
                launch_arguments={"use_sim_time": "true"}.items(),
            ),
            IncludeLaunchDescription(PythonLaunchDescriptionSource(os.path.join(projects, "projects_spawn_turtlebot3_bucket.launch.py"))),
            Node(
                package="rviz2",
                executable="rviz2",
                arguments=["-d", os.path.join(tb3_gazebo, "rviz", "tb3_gazebo.rviz")],
                parameters=[{"use_sim_time": True}],
                condition=IfCondition(rviz),
            ),
        ]
    )
