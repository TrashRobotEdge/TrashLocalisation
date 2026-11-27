cmake_minimum_required(VERSION 3.8)
project(trash_description)

find_package(ament_cmake REQUIRED)

# Data-only package: worlds and launch files go to share/. The URDF work (#8, #9) adds urdf/ here.
install(DIRECTORY worlds launch
  DESTINATION share/${PROJECT_NAME})

ament_package()
