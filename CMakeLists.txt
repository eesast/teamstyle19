cmake_minimum_required(VERSION 3.8)
project(communicate)

set(CMAKE_CXX_STANDARD 98)

set(SOURCE_FILES player_files/main.cpp player_files/communicate.h player_files/communicate_unix.cpp player_files/communicate.cpp)
add_executable(communicate ${SOURCE_FILES})