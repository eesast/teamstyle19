cmake_minimum_required(VERSION 3.8)
project(communicate)

set(CMAKE_CXX_STANDARD 17)

set(SOURCE_FILES main.cpp communicate.h api_player.h api_player.cpp communicate_unix.cpp communicate.cpp)
add_executable(communicate ${SOURCE_FILES})
