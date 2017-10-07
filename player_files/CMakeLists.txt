cmake_minimum_required(VERSION 3.8)
project(communicate)

set(CMAKE_CXX_STANDARD 98)

set(SOURCE_FILES main.cpp communicate.h communicate_unix.cpp communicate.cpp)
add_executable(communicate1 ${SOURCE_FILES})