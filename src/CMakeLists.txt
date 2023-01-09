
set(PLUGIN_NAME usdOpenAssetIOResolver)

set(
  SRC
    resolver.cpp
)

add_library(${PLUGIN_NAME}
    SHARED
    ${SRC}
)

find_package(PythonLibs REQUIRED)

target_link_libraries(${PLUGIN_NAME}
    PUBLIC
    ar
)

install(
    TARGETS
        ${PLUGIN_NAME}
    DESTINATION
        .
)
