set(HEADERS_DIR ../include/glucent)

set("${PROJECT_NAME}_HEADERS"
        ${HEADERS_DIR}/glucent.h)

set("${PROJECT_NAME}_SOURCES"
        gl.c glucent.cpp)

add_library(${PROJECT_NAME} ${GLUCENT_LIBRARY_TYPE}
        ${${PROJECT_NAME}_SOURCES}
        ${${PROJECT_NAME}_HEADERS})

target_include_directories(${PROJECT_NAME}
        PRIVATE
        ${PROJECT_SOURCE_DIR}/include

        PUBLIC
        $<BUILD_INTERFACE:${PROJECT_SOURCE_DIR}/include>
        $<INSTALL_INTERFACE:${CMAKE_INSTALL_INCLUDEDIR}>)