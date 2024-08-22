cmake . -Bbuild -G "Visual Studio 17 2022" -A Win32
cmake --build build --config Release

cmake . -Bbuild64 -G "Visual Studio 17 2022"  -A x64
cmake --build build64 --config Release --target PIMETextService