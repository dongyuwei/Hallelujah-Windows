set CMAKE_POLICY_VERSION_MINIMUM=3.5
cmake . -Bbuild -A Win32
cmake --build build --config Release

cmake . -Bbuild64 -A x64
cmake --build build64 --config Release --target PIMETextService