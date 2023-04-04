add_subdirectory(triangle)

set(GLFW_BUILD_DOCS OFF CACHE BOOL "" FORCE)
set(GLFW_BUILD_TESTS OFF CACHE BOOL "" FORCE)
set(GLFW_BUILD_EXAMPLES OFF CACHE BOOL "" FORCE)
add_subdirectory(deps/glfw EXCLUDE_FROM_ALL)

add_compile_definitions(GLFW_INCLUDE_NONE)