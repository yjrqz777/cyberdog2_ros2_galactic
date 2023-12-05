# generated from ament/cmake/core/templates/nameConfig.cmake.in

# prevent multiple inclusion
if(_moto_contor_test_CONFIG_INCLUDED)
  # ensure to keep the found flag the same
  if(NOT DEFINED moto_contor_test_FOUND)
    # explicitly set it to FALSE, otherwise CMake will set it to TRUE
    set(moto_contor_test_FOUND FALSE)
  elseif(NOT moto_contor_test_FOUND)
    # use separate condition to avoid uninitialized variable warning
    set(moto_contor_test_FOUND FALSE)
  endif()
  return()
endif()
set(_moto_contor_test_CONFIG_INCLUDED TRUE)

# output package information
if(NOT moto_contor_test_FIND_QUIETLY)
  message(STATUS "Found moto_contor_test: 0.0.0 (${moto_contor_test_DIR})")
endif()

# warn when using a deprecated package
if(NOT "" STREQUAL "")
  set(_msg "Package 'moto_contor_test' is deprecated")
  # append custom deprecation text if available
  if(NOT "" STREQUAL "TRUE")
    set(_msg "${_msg} ()")
  endif()
  # optionally quiet the deprecation message
  if(NOT ${moto_contor_test_DEPRECATED_QUIET})
    message(DEPRECATION "${_msg}")
  endif()
endif()

# flag package as ament-based to distinguish it after being find_package()-ed
set(moto_contor_test_FOUND_AMENT_PACKAGE TRUE)

# include all config extra files
set(_extras "ament_cmake_export_libraries-extras.cmake;ament_cmake_export_dependencies-extras.cmake")
foreach(_extra ${_extras})
  include("${moto_contor_test_DIR}/${_extra}")
endforeach()
