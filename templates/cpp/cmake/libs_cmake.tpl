# This project is licensed under the {license} license. For more information
# see the LICENSE file.

cmake_minimum_required(VERSION 2.8)

# ------------------------------------------------------------------------------

set(PROJ_CPP_VERSION 14)
add_definitions(-DCPP_VERSION=${PROJ_CPP_VERSION})

set(CMAKE_BINARY_DIR ${CMAKE_CURRENT_SOURCE_DIR}/../build)
set(EXECUTABLE_OUTPUT_PATH ${CMAKE_BINARY_DIR})
set(LIBRARY_OUTPUT_PATH ${CMAKE_BINARY_DIR})

# ------------------------------------------------------------------------------

set(LIBS_INCLUDE_DIRS
# -- googletest / -mock --------------------------------------------------------
  ${CMAKE_CURRENT_SOURCE_DIR}/gtest/googletest/include
  ${CMAKE_CURRENT_SOURCE_DIR}/gtest/googlemock/include
# ------------------------------------------------------------------------------
PARENT_SCOPE)

message(STATUS "added ${White}gtest")

# ------------------------------------------------------------------------------

set(LIBS_SRC_FILES
PARENT_SCOPE)

set(PROJ_LIBS
PARENT_SCOPE)
