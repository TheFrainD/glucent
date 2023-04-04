cmake_minimum_required(VERSION 3.16)
project(glucent VERSION 1.0.0)

set(CMAKE_CXX_STANDARD 20)

find_package(OpenGL REQUIRED)

list(APPEND CMAKE_MODULE_PATH "${PROJECT_SOURCE_DIR}/cmake")

set_property(GLOBAL PROPERTY USE_FOLDERS ON)

option(BUILD_SHARED_LIBS "Build shored libraries" OFF) # Not suppoeted
option(GLUCENT_BUILD_EXAMPLES "Build glucent examples" ON)
option(GLUCENT_BUILD_DOCS "Build glucent documentation" ON) # Not implemented
option(GLUCENT_INSTALL "Generate installation target" ON) # Not implemented

include(Config)

if(BUILD_SHARED_LIBS)
    message(FATAL_ERROR "Building shared lib is not supported")
    return()
else()
    set(GLUCENT_LIBRARY_TYPE "STATIC")
endif()

add_subdirectory(src)

add_subdirectory(examples)
