cmake_minimum_required(VERSION 3.16)
project(glucent VERSION 1.0.0)

list(APPEND CMAKE_MODULE_PATH "${PROJECT_SOURCE_DIR}/cmake")

set_property(GLOBAL PROPERTY USE_FOLDERS ON)

option(BUILD_SHARED_LIBS "Build shored libraries" OFF)
option(GLUCENT_BUILD_EXAMPLES "Build glucent examples" OFF)
option(GLUCENT_BUILD_DOCS "Build glucent documentation" ON)
option(GLUCENT_INSTALL "Generate installation target" ON)

include(Config)

include(GNUInstallDirs)

add_subdirectory(src)

if (GLUCENT_BUILD_EXAMPLES) 
    add_subdirectory(examples)
endif()