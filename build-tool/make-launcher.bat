@echo off

mkdir build
mkdir ..\dist

cd build
windres -i ..\icon\icon-win.rc .\icon.o
g++ ..\launcher\launcher-win.cpp .\icon.o -static -o .\launcher.exe
move .\launcher.exe ..\..\dist\

cd ..
rmdir /s/q build

echo "Success. Product is in ..\dist\"
