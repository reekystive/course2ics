mkdir build
mkdir ../dist

cd build
python3 -m venv venv
source ./venv/bin/activate
pip list

pip install -i https://pypi.tuna.tsinghua.edu.cn/simple -r ../../requirements.txt
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple pyinstaller

mkdir product
cd product
pyinstaller ../../../main.py
deactivate

mv ./dist/main ../../../dist/bin
cp ../../../config.ini ../../../dist/

cd ..
cd ..
rm -r build
rm -r ../__pycache__

echo "Success. Product is in ../dist/"
