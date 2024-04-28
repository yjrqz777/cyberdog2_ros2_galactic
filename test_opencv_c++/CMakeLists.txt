cmake_minimum_required( VERSION 2.8 )

# 声明一个 cmake 工程
project(opencv_learn)

# 设置编译模式
#set( CMAKE_BUILD_TYPE "Debug" )

#添加OPENCV库
#指定OpenCV版本，代码如下
#find_package(OpenCV 4.2 REQUIRED)
#如果不需要指定OpenCV版本，代码如下
find_package(OpenCV REQUIRED)

include_directories(
 ./include/
 )


#添加OpenCV头文件
include_directories(${OpenCV_INCLUDE_DIRS})

#显示OpenCV_INCLUDE_DIRS的值
message(${OpenCV_INCLUDE_DIRS})

FILE(GLOB_RECURSE TEST_SRC
 src/main.cpp
 #src/*.c
#  3.png
#  ${CMAKE_SOURCE_DIR}/*.cpp
#  ${CMAKE_SOURCE_DIR}/*.cp
 )
# message(${CMAKE_SOURCE_DIR})
# 添加一个可执行程序
# 语法：add_executable( 程序名 源代码文件 ）
add_executable(target ${TEST_SRC})


set(libs 
/SDCARD/workspace/cyberdog2_ros2_galactic/test_opencv_c++/lib/libAudioRender.so
/SDCARD/workspace/cyberdog2_ros2_galactic/test_opencv_c++/lib/libcrypto.so
/SDCARD/workspace/cyberdog2_ros2_galactic/test_opencv_c++/lib/libcrypto.so.1.1
/SDCARD/workspace/cyberdog2_ros2_galactic/test_opencv_c++/lib/libHCCore.so
/SDCARD/workspace/cyberdog2_ros2_galactic/test_opencv_c++/lib/libhcnetsdk.so
/SDCARD/workspace/cyberdog2_ros2_galactic/test_opencv_c++/lib/libhpr.so
/SDCARD/workspace/cyberdog2_ros2_galactic/test_opencv_c++/lib/libPlayCtrl.so
/SDCARD/workspace/cyberdog2_ros2_galactic/test_opencv_c++/lib/libssl.so
/SDCARD/workspace/cyberdog2_ros2_galactic/test_opencv_c++/lib/libssl.so.1.1
/SDCARD/workspace/cyberdog2_ros2_galactic/test_opencv_c++/lib/libSuperRender.so
/SDCARD/workspace/cyberdog2_ros2_galactic/test_opencv_c++/lib/libz.so
)

# 将库文件链接到可执行程序上
message(${OpenCV_LIBS})
target_link_libraries(target PRIVATE ${libs} ${OpenCV_LIBS})

# target_link_libraries(target  ${OpenCV_LIBS})