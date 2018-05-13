# This project is licensed under the {license} license. For more information
# see the LICENSE file.

cmake_minimum_required(VERSION 2.8)

project({technicalTitle})

# ------------------------------------------------------------------------------

set(CMAKE_MODULE_PATH "${CMAKE_SOURCE_DIR}/cmake")
include(colorize)

# ------------------------------------------------------------------------------

message(STATUS "${BoldGreen}----------------------------------------")
message(STATUS "${BoldGreen}configuring build for {technicalTitle}")
message(STATUS "${BoldGreen}----------------------------------------")

# ------------------------------------------------------------------------------

include(cotire)

# ------------------------------------------------------------------------------

# this should only be set to true, if you want to run the tests
set(PROJ_UNIT_TESTS true)

# ------------------------------------------------------------------------------

if (PROJ_UNIT_TESTS)
  enable_testing()
  add_definitions(-DUNIT_TESTS)
  message(STATUS "with ${BoldGreen}UNIT_TESTS${ColorReset}${Green} defined")
endif()

# ------------------------------------------------------------------------------

set(PROJ_CPP_VERSION 14)
add_definitions(-DCPP_VERSION=${PROJ_CPP_VERSION})

# ------------------------------------------------------------------------------

set(CMAKE_BINARY_DIR ${CMAKE_CURRENT_SOURCE_DIR}/build)
set(EXECUTABLE_OUTPUT_PATH ${CMAKE_BINARY_DIR})
set(LIBRARY_OUTPUT_PATH ${CMAKE_BINARY_DIR})

# ------------------------------------------------------------------------------

set(PROJ_INCLUDE_DIR ${PROJECT_SOURCE_DIR}/include)
file(GLOB_RECURSE PROJ_SRC_FILES ${PROJECT_SOURCE_DIR}/src/{technicalTitle}/*.cpp)
file(GLOB_RECURSE PROJ_TESTS_FILES ${CMAKE_CURRENT_SOURCE_DIR}/tests/*.cpp)

# ------------------------------------------------------------------------------

set(
  CMAKE_CXX_FLAGS
  "${CMAKE_CXX_FLAGS} -g -std=c++${PROJ_CPP_VERSION} -Wall -Wpedantic -Wextra -Wno-ignored-qualifiers -fno-rtti -fno-exceptions -fsanitize=address -fno-omit-frame-pointer"
)

# ------------------------------------------------------------------------------

if (UNIX AND NOT APPLE)
  execute_process(COMMAND ${CMAKE_CXX_COMPILER}
    -fuse-ld=gold -Wl,--version
    ERROR_QUIET OUTPUT_VARIABLE ld_version
  )

  if ("${ld_version}" MATCHES "GNU gold")
    message(STATUS "Found Gold linker, use faster linker")
    set(CMAKE_EXE_LINKER_FLAGS
      "${CMAKE_EXE_LINKER_FLAGS} -fuse-ld=gold"
    )
    set(CMAKE_SHARED_LINKER_FLAGS
      "${CMAKE_SHARED_LINKER_FLAGS} -fuse-ld=gold "
    )
  endif()
endif()

# ------------------------------------------------------------------------------

message(STATUS "${BoldGreen}------- configuring libraries")

if (PROJ_UNIT_TESTS)
  set(gtest_force_shared_crt ON CACHE BOOL "" FORCE)
  add_subdirectory(${CMAKE_CURRENT_SOURCE_DIR}/libs/gtest/googlemock)
endif()

add_subdirectory(libs)

message(STATUS "${BoldGreen}------- configuring libraries done")

# ------------------------------------------------------------------------------

if (PROJ_UNIT_TESTS)
  include_directories(
    ${LIBS_INCLUDE_DIRS}
    ${PROJ_INCLUDE_DIR}
    ${CMAKE_CURRENT_SOURCE_DIR}/tests
  )
else()
  include_directories(
    ${LIBS_INCLUDE_DIRS}
    ${PROJ_INCLUDE_DIR}
  )
endif()

# ------------------------------------------------------------------------------

add_library({technicalTitle}library STATIC ${PROJ_SRC_FILES} ${LIBS_SRC_FILES})
target_link_libraries({technicalTitle}library
  ${PROJ_LIBS}
)

# ------------------------------------------------------------------------------

if (PROJ_UNIT_TESTS)
  add_executable(
    {technicalTitle}Tests
      ${PROJ_TESTS_FILES}
  )
  target_link_libraries({technicalTitle}Tests gmock_main {technicalTitle}library)
  add_test({technicalTitle}Tests ${CMAKE_CURRENT_SOURCE_DIR}/build/{technicalTitle}Tests)
endif()

# ------------------------------------------------------------------------------

cotire({technicalTitle}library {technicalTitle}Tests)
