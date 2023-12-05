# generated from ament/cmake/core/templates/nameConfig.cmake.in

# prevent multiple inclusion
if(_talk_something_CONFIG_INCLUDED)
  # ensure to keep the found flag the same
  if(NOT DEFINED talk_something_FOUND)
    # explicitly set it to FALSE, otherwise CMake will set it to TRUE
    set(talk_something_FOUND FALSE)
  elseif(NOT talk_something_FOUND)
    # use separate condition to avoid uninitialized variable warning
    set(talk_something_FOUND FALSE)
  endif()
  return()
endif()
set(_talk_something_CONFIG_INCLUDED TRUE)

# output package information
if(NOT talk_something_FIND_QUIETLY)
  message(STATUS "Found talk_something: 0.0.0 (${talk_something_DIR})")
endif()

# warn when using a deprecated package
if(NOT "" STREQUAL "")
  set(_msg "Package 'talk_something' is deprecated")
  # append custom deprecation text if available
  if(NOT "" STREQUAL "TRUE")
    set(_msg "${_msg} ()")
  endif()
  # optionally quiet the deprecation message
  if(NOT ${talk_something_DEPRECATED_QUIET})
    message(DEPRECATION "${_msg}")
  endif()
endif()

# flag package as ament-based to distinguish it after being find_package()-ed
set(talk_something_FOUND_AMENT_PACKAGE TRUE)

# include all config extra files
set(_extras "ament_cmake_export_include_directories-extras.cmake;ament_cmake_export_dependencies-extras.cmake")
foreach(_extra ${_extras})
  include("${talk_something_DIR}/${_extra}")
endforeach()
