echo "Compile Qt GUI files"
pyuic5 -x src/gui/mainwindow.ui -o src/gui/ui_mainwindow.py
pyrcc5 src/resources.qrc -o src/resources.py

echo "Build distribution"
rm -r dist
rm -r build
cd src

# LD_LIBRARY_PATH=path_to_python_libs
pyinstaller ActiveImageLabeler.py --distpath ./../dist --workpath ./../build 
# LD_LIBRARY_PATH=/home/ramazam/Downloads/yes/lib pyinstaller  ActiveImageLabeler.py --distpath ./../dist --workpath ./../build --hidden-import=PyQt5
# pyinstaller -F src/ActiveImageLabeler.py
# LD_LIBRARY_PATH=/home/ramazam/Downloads/yes/lib pyinstaller -F ActiveImageLabeler.py --distpath ./../dist --workpath ./../build --hidden-import=torchvision --hidden-import=torch

echo "Run distribution"
./dist/ActiveImageLabeler
