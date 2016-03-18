cmake_minimum_required(VERSION 2.8.3)
project(hector_senseair_s8_driver)

## Find catkin macros and libraries
## if COMPONENTS list like find_package(catkin REQUIRED COMPONENTS xyz)
## is used, also find other catkin packages
find_package(catkin REQUIRED COMPONENTS
  rospy
  std_msgs
)

catkin_python_setup()

catkin_package(
    INCLUDE_DIRS src
  CATKIN_DEPENDS std_msgs)

  FILE(GLOB BIN_FILES "bin/*")

  # install executables
  install(PROGRAMS ${BIN_FILES} DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION})
  install(DIRECTORY launch DESTINATION ${CATKIN_PACKAGE_SHARE_DESTINATION})
