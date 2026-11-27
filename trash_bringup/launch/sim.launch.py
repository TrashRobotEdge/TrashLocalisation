"""The whole baseline in sim: world + robot + detector + localiser + approach.

    ros2 launch trash_bringup sim.launch.py [variant:=hsv-red] [world:=cans.sdf] [rviz:=true]

Node settings live in each package's config/*.yaml; only the switches are launch arguments.
"""

import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def config(package, name):
    return os.path.join(get_package_share_directory(package), "config", name)


def generate_launch_description():
    sim = os.path.join(get_package_share_directory("trash_description"), "launch", "sim.launch.py")
    sim_time = {"use_sim_time": True}

    return LaunchDescription(
        [
            DeclareLaunchArgument(
                "variant",
                default_value="yolov8n-coco-640-fp32-onnx",
                description="edgetrash model variant (EdgeTrash models/manifest.yaml), e.g. hsv-red",
            ),
            DeclareLaunchArgument("world", default_value="cans.sdf"),
            DeclareLaunchArgument("rviz", default_value="false"),
            IncludeLaunchDescription(
                PythonLaunchDescriptionSource(sim),
                launch_arguments={"world": LaunchConfiguration("world"), "rviz": LaunchConfiguration("rviz")}.items(),
            ),
            Node(
                package="trash_detector",
                executable="detector",
                output="screen",
                parameters=[config("trash_detector", "detector.yaml"), {"variant": LaunchConfiguration("variant")}, sim_time],
            ),
            Node(
                package="trash_localizer",
                executable="localizer",
                output="screen",
                parameters=[config("trash_localizer", "localizer.yaml"), sim_time],
            ),
            Node(
                package="trash_behaviour",
                executable="approach",
                output="screen",
                parameters=[config("trash_behaviour", "approach.yaml"), sim_time],
            ),
        ]
    )
