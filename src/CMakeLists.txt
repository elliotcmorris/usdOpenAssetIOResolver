
set(PLUGIN_NAME usdOpenAssetIOResolver)

set(
  SRC
    resolver.cpp
)

add_library(${PLUGIN_NAME}
    SHARED
    ${SRC}
)

target_link_libraries(${PLUGIN_NAME}
    PUBLIC
    ar
)

#-----------------------------------------------------------------------
# Activate warnings as errors, pedantic, etc.
include(CompilerWarnings)
set_default_compiler_warnings(${PLUGIN_NAME})

#-----------------------------------------------------------------------
# Activate Static Analysis
include(StaticAnalyzers)
if (OPENASSETIO_ENABLE_CLANG_FORMAT)
    enable_clang_format()
    add_dependencies(${PLUGIN_NAME} openassetio-clangformat)
endif ()
if (OPENASSETIO_ENABLE_CLANG_TIDY)
    enable_clang_tidy()
endif ()
if (OPENASSETIO_ENABLE_CPPLINT)
    enable_cpplint()
    add_dependencies(${PLUGIN_NAME} openassetio-cpplint)
endif ()

#-----------------------------------------------------------------------
# Main install
install(
    TARGETS
        ${PLUGIN_NAME}
    DESTINATION
        .
)

#-----------------------------------------------------------------------
# Install plugInfo.json
install(
    FILES
		resources/plugInfo.json
    DESTINATION
        ./resources
)
