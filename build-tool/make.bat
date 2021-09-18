@echo off

mkdir build
mkdir ..\dist

cd build
python -m venv venv
CALL .\venv\Scripts\activate.bat
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple -r ..\..\requirements.txt
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple pyinstaller

mkdir product
cd product
pyinstaller ..\..\..\main.py --icon ..\..\icon\icon-win.ico
CALL deactivate

xcopy /e/y .\dist\main\ ..\..\..\dist\bin\
copy ..\..\..\config.ini ..\..\..\dist\

cd ..
cd ..
rmdir /s/q build
rmdir /s/q ..\__pycache__

echo "Success. Product is in ..\dist\"
