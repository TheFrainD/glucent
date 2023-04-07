cmake_minimum_required(VERSION 3.16)
project(glucent VERSION 0.1.0)

set(CMAKE_CXX_STANDARD 20)

find_package(OpenGL REQUIRED)

list(APPEND CMAKE_MODULE_PATH "${PROJECT_SOURCE_DIR}/cmake")

set_property(GLOBAL PROPERTY USE_FOLDERS ON)

option(BUILD_SHARED_LIBS "Build shored libraries" OFF) # Not supported
option(GLUCENT_BUILD_EXAMPLES "Build glucent examples" OFF)
option(GLUCENT_BUILD_DOCS "Build glucent documentation" ON) # Not implemented
option(GLUCENT_INSTALL "Generate installation target" ON)

include(GNUInstallDirs)
include(CMakeDependentOption)

if(BUILD_SHARED_LIBS)
    message(FATAL_ERROR "Building shared lib is not supported")
    return()
else()
    set(GLUCENT_LIBRARY_TYPE "STATIC")
endif()

include(CMakePackageConfigHelpers)

set(GLUCENT_CONFIG_PATH "${CMAKE_INSTALL_LIBDIR}/cmake/glucent")

configure_package_config_file(cmake/glucentConfig.cmake.in
        src/glucentConfig.cmake
        INSTALL_DESTINATION ${GLUCENT_CONFIG_PATH}
        NO_CHECK_REQUIRED_COMPONENTS_MACRO)

write_basic_package_version_file(src/glucentConfigVersion.cmake
        VERSION ${PROJECT_VERSION}
        COMPATIBILITY SameMajorVersion)

add_subdirectory(src)

if (GLUCENT_BUILD_EXAMPLES)
    add_subdirectory(examples)
endif()

if (GLUCENT_INSTALL)
    install(DIRECTORY include DESTINATION ${CMAKE_INSTALL_INCLUDEDIR})

    install(FILES ${PROJECT_BINARY_DIR}/src/glucentConfig.cmake
            ${PROJECT_BINARY_DIR}/src/glucentConfigVersion.cmake
            DESTINATION ${GLUCENT_CONFIG_PATH})

    install(EXPORT glucentTargets FILE glucentTargets.cmake
            EXPORT_LINK_INTERFACE_LIBRARIES
            DESTINATION ${GLUCENT_CONFIG_PATH})

    install(FILES ${PROJECT_BINARY_DIR}/src/glucent.pc
            DESTINATION ${PROJECT_BINARY_DIR}/src)
endif()
