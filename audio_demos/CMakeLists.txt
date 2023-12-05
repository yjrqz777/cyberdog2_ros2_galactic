cmake_minimum_required(VERSION 3.8)
project(audio_demos)

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic -g)
endif()

# find dependencies
find_package(ament_cmake REQUIRED)
find_package(ament_index_cpp REQUIRED)
find_package(rclcpp REQUIRED)
find_package(rclcpp_components REQUIRED)
find_package(std_msgs REQUIRED)
find_package(std_srvs REQUIRED)
find_package(protocol REQUIRED)

set(dependencies
  rclcpp
  rclcpp_components
  std_srvs
  std_msgs
  ament_index_cpp
  protocol
)
include_directories(include)

add_executable(talker
  src/talker.cpp)
ament_target_dependencies(talker
  rclcpp
  std_srvs
  std_msgs
  protocol
  ament_index_cpp
)
add_executable(set_mic
  src/set_mic.cpp)
ament_target_dependencies(set_mic
  rclcpp
  std_srvs
  std_msgs
  protocol
  ament_index_cpp
)
add_executable(set_voice
  src/set_voice.cpp)
ament_target_dependencies(set_voice
  rclcpp
  std_srvs
  std_msgs
  protocol
  ament_index_cpp
)
add_executable(set_waken_words
  src/set_waken_words.cpp)

ament_target_dependencies(set_waken_words
  rclcpp
  std_srvs
  std_msgs
  protocol
  ament_index_cpp
)

install(TARGETS
  talker
  set_mic
  set_voice
  set_waken_words
  DESTINATION lib/${PROJECT_NAME})



if(BUILD_TESTING)
  find_package(ament_lint_auto REQUIRED)
  # the following line skips the linter which checks for copyrights
  # uncomment the line when a copyright and license is not present in all source files
  #set(ament_cmake_copyright_FOUND TRUE)
  # the following line skips cpplint (only works in a git repo)
  # uncomment the line when this package is not in a git repo
  #set(ament_cmake_cpplint_FOUND TRUE)
  ament_lint_auto_find_test_dependencies()
endif()

# ament_export_lib
ament_export_include_directories(include)
ament_export_dependencies(${dependencies})
ament_package()
