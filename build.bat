rem allow old cmake_minimum_required() declarations to work with CMake 4.x
set CMAKE_POLICY_VERSION_MINIMUM=3.5
cmake . -Bbuild -G"Visual Studio 16 2019" -A Win32
cmake --build build --config Release

cmake . -Bbuild64 -G"Visual Studio 16 2019" -A x64
cmake --build build64 --config Release --target PIMETextService
