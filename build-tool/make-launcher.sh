mkdir build
mkdir ../dist

cd build
clang++ ../launcher/launcher-macos.cpp -o ./launcher

mv ./launcher ../../dist
cd ..
rm -r build

echo "Success. Product is in ../dist/"
