add_library(glucent ${GLUCENT_LIBRARY_TYPE}
        ${PROJECT_SOURCE_DIR}/include/glucent/glucent.h
        ${PROJECT_SOURCE_DIR}/include/GL/gl.h
        ${PROJECT_SOURCE_DIR}/include/GL/glcorearb.h
        ${PROJECT_SOURCE_DIR}/include/KHR/khrplatform.h
        gl.c glucent.cpp)

set(GLUCENT_LIB_NAME glucent)

set_target_properties(
        glucent PROPERTIES
        OUTPUT_NAME ${GLUCENT_LIB_NAME}
        VERSION ${PROJECT_VERSION_MAJOR}}.${PROJECT_VERSION_MINOR}
        SOVERSION ${PROJECT_VERSION_MAJOR}
        POSITION_INDEPENDENT_CODE ON
        C_STANDARD 99
        CXX_STANDARD 17
        C_EXTENSIONS OFF
        DEFINE_SYMBOL _GLUCENT_BUILD_DLL
        FOLDER "glucent")

target_include_directories(glucent PUBLIC
        "$<BUILD_INTERFACE:${PROJECT_SOURCE_DIR}/include>"
        "$<INSTALL_INTERFACE:${CMAKE_INSTALL_INCLUDEDIR}>")

set(GLFW_PKG_CONFIG_REQUIRES_PRIVATE "${deps}" CACHE INTERNAL
        "GLFW pkg-config Requires.private")
set(GLFW_PKG_CONFIG_LIBS_PRIVATE "${libs}" CACHE INTERNAL
        "GLFW pkg-config Libs.private")

configure_file(${PROJECT_SOURCE_DIR}/cmake/glucent.pc.in glucent.pc @ONLY)

if (GLUCENT_INSTALL)
    install(TARGETS glucent
            EXPORT glucentTargets
            RUNTIME DESTINATION "${CMAKE_INSTALL_BINDIR}"
            ARCHIVE DESTINATION "${CMAKE_INSTALL_LIBDIR}"
            LIBRARY DESTINATION "${CMAKE_INSTALL_LIBDIR}")
endif()
