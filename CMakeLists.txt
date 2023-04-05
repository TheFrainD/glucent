cmake_minimum_required(VERSION 3.16)
project(glucent VERSION 0.1.0)

set(CMAKE_CXX_STANDARD 20)

find_package(OpenGL REQUIRED)

list(APPEND CMAKE_MODULE_PATH "${PROJECT_SOURCE_DIR}/cmake")

set_property(GLOBAL PROPERTY USE_FOLDERS ON)

option(BUILD_SHARED_LIBS "Build shored libraries" OFF) # Not supported
option(GLUCENT_BUILD_EXAMPLES "Build glucent examples" OFF)
option(GLUCENT_BUILD_DOCS "Build glucent documentation" ON) # Not implemented
option(GLUCENT_INSTALL "Generate installation target" ON) # Not implemented

set(CMAKE_POSITION_INDEPENDENT_CODE ON)

if(BUILD_SHARED_LIBS)
    message(FATAL_ERROR "Building shared lib is not supported")
    return()
else()
    set(GLUCENT_LIBRARY_TYPE "STATIC")
endif()

set(SOURCE_DIR ${CMAKE_CURRENT_SOURCE_DIR}/src)
set(HEADERS_DIR ${CMAKE_CURRENT_SOURCE_DIR}/include)

set("${PROJECT_NAME}_HEADERS"
        ${HEADERS_DIR}/glucent/glucent.h
        ${HEADERS_DIR}/GL/gl.h
        ${HEADERS_DIR}/GL/glcorearb.h
        ${HEADERS_DIR}/KHR/khrplatform.h)

set("${PROJECT_NAME}_SOURCES"
        ${SOURCE_DIR}/gl.c
        ${SOURCE_DIR}/glucent.cpp)

add_library(${PROJECT_NAME} ${GLUCENT_LIBRARY_TYPE}
        ${${PROJECT_NAME}_SOURCES}
        ${${PROJECT_NAME}_HEADERS})

include(GNUInstallDirs)

set(GLUCENT_INSTALL_DIR "/${CMAKE_INSTALL_LIBDIR}/pkgconfig")

target_include_directories(${PROJECT_NAME}
        PRIVATE
        ${HEADERS_DIR}

        PUBLIC
        $<BUILD_INTERFACE:${HEADERS_DIR}>
        $<INSTALL_INTERFACE:${CMAKE_INSTALL_INCLUDEDIR}>)

install(DIRECTORY ${HEADERS_DIR}
        DESTINATION include)

install(TARGETS ${PROJECT_NAME}
        EXPORT ${PROJECT_NAME}-config
        ARCHIVE DESTINATION lib)

include(CMakePackageConfigHelpers)
configure_package_config_file(${CMAKE_CURRENT_SOURCE_DIR}/cmake/config.cmake.in
        ${CMAKE_CURRENT_BINARY_DIR}/${PROJECT_NAME}-config.cmake
        INSTALL_DESTINATION lib/cmake/${PROJECT_NAME})

# Install the CMake package configuration file and export set
install(EXPORT ${PROJECT_NAME}-config
        NAMESPACE ${PROJECT_NAME}::
        DESTINATION lib/cmake/${PROJECT_NAME})

install(FILES ${CMAKE_CURRENT_BINARY_DIR}/${PROJECT_NAME}-config.cmake
        DESTINATION lib/cmake/${PROJECT_NAME})

if (GLUCENT_BUILD_EXAMPLES)
    add_subdirectory(examples)
endif()
