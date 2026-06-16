cmake_minimum_required(VERSION 4.3.2)

project(
    WeightedMatching
    VERSION 1.0.0
    SPDX_LICENSE "MIT"
    DESCRIPTION "Analysis of weighted matching algorithms."
    LANGUAGES "CXX"
)

add_executable(main)

target_sources(
    main
    PRIVATE
    src/main.cpp
)


target_include_directories(
    main
    PRIVATE
    src/include
)

if(LOG)
    target_compile_definitions(main PRIVATE LOG)
endif()

if(CMAKE_CXX_COMPILER_FRONTEND_VARIANT STREQUAL "MSVC")
    target_compile_options(main PRIVATE /W3 /WX)
endif()
