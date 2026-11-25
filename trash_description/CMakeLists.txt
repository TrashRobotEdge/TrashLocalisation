cmake_minimum_required(VERSION 3.8)
project(trash_description)

find_package(ament_cmake REQUIRED)

# Data-only package: URDF, worlds and launch files are installed to share/.
install(DIRECTORY urdf worlds launch
  DESTINATION share/${PROJECT_NAME})

ament_package()
