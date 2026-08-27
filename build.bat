rem allow old cmake_minimum_required() declarations to work with CMake 4.x
set CMAKE_POLICY_VERSION_MINIMUM=3.5
rem no -G: let cmake auto-detect the installed Visual Studio (VS2019 on AppVeyor, VS2026 on GitHub CI)
cmake . -Bbuild -A Win32
cmake --build build --config Release

cmake . -Bbuild64 -A x64
cmake --build build64 --config Release --target PIMETextService
