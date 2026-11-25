from glob import glob

from setuptools import find_packages, setup

package_name = 'trash_localizer'

setup(
    name=package_name,
    version='0.0.1',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages', ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='TrashRobotEdge',
    maintainer_email='trashrobotedge@users.noreply.github.com',
    description='Turns 2D detections + depth + camera_info into a 3D target pose in the odom frame (TF2).',
    license='TODO',
    entry_points={
        'console_scripts': [
            # 'node_name = trash_localizer.module:main',
        ],
    },
)
