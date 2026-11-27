from glob import glob

from setuptools import find_packages, setup

package_name = "trash_behaviour"

setup(
    name=package_name,
    version="0.0.1",
    packages=find_packages(exclude=["test"]),
    data_files=[
        ("share/ament_index/resource_index/packages", ["resource/" + package_name]),
        ("share/" + package_name, ["package.xml"]),
        ("share/" + package_name + "/config", glob("config/*.yaml")),
    ],
    install_requires=["setuptools"],
    zip_safe=True,
    maintainer="TrashRobotEdge",
    maintainer_email="trashrobotedge@users.noreply.github.com",
    description="Drives the robot to the target, lidar safety stop.",
    license="TODO",
    entry_points={
        "console_scripts": [
            "approach = trash_behaviour.approach_node:main",
        ]
    },
)
